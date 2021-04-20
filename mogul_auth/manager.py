# mogul_auth/manager.py
from subscriptions.management.commands import _manager
from decimal import Decimal as D
from django.db.models import Q
from oscar_accounts import models, exceptions, facade
from django.utils import timezone
from subscriptions import models as submodels
from notifications.signals import notify

class YetiManager(_manager.Manager):

    def process_payment(self, user, cost):
        accounts = models.Account.active.filter(primary_user=user).order_by('-name')
        transfers = []
        amount_to_allocate = cost.cost
        for account in accounts:
            to_transfer = min(account.balance, amount_to_allocate)
            transfers.append((account, to_transfer))
            amount_to_allocate -= to_transfer
            if amount_to_allocate == D('0.00'):
                break
        if amount_to_allocate > D('0.00'):
            return False

        # Execute transfers to some 'Sales' account
        destination, _ = models.Account.objects.get_or_create(name="Subscriptions")
        completed_transfers = []
        try:
            for account, amount in transfers:
                transfer = facade.transfer(
                    source=account,
                        destination=destination,
                        amount=D(amount),
                    description="Subscription %s" % cost.slug)
                completed_transfers.append(transfer)

        except exceptions.AccountException:
            # Something went wrong with one of the transfers (possibly a race condition).
            # We try and roll back all completed ones to get us back to a clean state.
            try:
                for transfer in completed_transfers:
                    facade.reverse(transfer)
            except Exception:
                # Uh oh: No man's land.  We could be left with a partial
                # redemption. This will require an admin to intervene.  Make
                # sure your logger mails admins on error.
                logger.error("Transfer failed")

            # Raise an exception so that your client code can inform the user appropriately.
            return False
        else:
            # All transfers completed ok
            return completed_transfers
        return False

    def process_due(self, subscription):
        """Handles processing of a due subscription.
            Parameters:
                subscription (obj): A UserSubscription instance.
        """
        user = subscription.user
        cost = subscription.subscription

        payment_transaction = self.process_payment(user=user, cost=cost)

        if payment_transaction:
            # Update subscription details
            current = timezone.now()
            next_billing = cost.next_billing_datetime(
                subscription.date_billing_next
            )
            subscription.date_billing_last = current
            subscription.date_billing_next = next_billing
            subscription.save()

            # Record the transaction details
            self.record_transaction(subscription,self.retrieve_transaction_date(payment_transaction))
            self.notify_payment_success(subscription)
            #
        #
        else:
            self.process_expired(subscription)
        return True

    def process_subscriptions(self):
        
        """Calls all required subscription processing functions."""
        current = timezone.now()

        # Handle new subscriptions
        new_subscriptions = submodels.UserSubscription.objects.filter(
            Q(active=False) & Q(cancelled=False)
            & Q(date_billing_start__lte=current)
        )

        for subscription in new_subscriptions:
            self.process_new(subscription)

        # Handle subscriptions with billing due
        due_subscriptions = submodels.UserSubscription.objects.filter(
            Q(active=True) & Q(cancelled=False)
            & Q(date_billing_next__lte=current)
        )

        for subscription in due_subscriptions:
            self.process_due(subscription)

    def notify_expired(self, subscription):
        """Sends notification of expired subscription.
            Parameters:
                subscription (obj): A UserSubscription instance.
        """
        user = subscription.user
        notify.send(subscription, recipient=user, verb=f"SubExpired",action_object=subscription)

    def notify_new(self, subscription):
        """Sends notification of newly active subscription
            Parameters:
                subscription (obj): A UserSubscription instance.
        """
        user = subscription.user
        notify.send(subscription, recipient=user, verb=f"SubActivated",action_object=subscription)

    def notify_payment_error(self, subscription):
        """Sends notification of a payment error
            Parameters:
                subscription (obj): A UserSubscription instance.
        """
        user = subscription.user
        notify.send(subscription, recipient=user, verb=f"SubPaymentError",action_object=subscription)

    def notify_payment_success(self, subscription):
        """Sends notifiation of a payment success
            Parameters:
                subscription (obj): A UserSubscription instance.
        """
        user = subscription.user
        notify.send(subscription, recipient=user, verb=f"SubPaymentSuccess",action_object=subscription)