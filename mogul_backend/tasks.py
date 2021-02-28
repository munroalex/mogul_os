# Create your tasks here

from celery import shared_task
from eveuniverse.models import EveType, EveRace, EveStation
from esi.clients import EsiClientProvider
from esi.decorators import single_use_token,token_required,tokens_required
from esi.models import Token
from django.conf import settings
from django.utils import timezone
from mogul_backend.models import Transaction, Character, Order, Structure, Stock,Profit
from django.contrib.auth.models import User
from mogul_backend.helpers.orm import BulkCreateManager
from mogul_backend.datehelpers import one_hour_ago,one_day_ago
from eveuniverse.helpers import EveEntityNameResolver
from notifications.signals import notify
import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from decimal import Decimal

esi = EsiClientProvider(spec_file='mogul_auth/swagger.json')

def first(iterable, default=None):
  for item in iterable:
    return item
  return default

@shared_task(name="importtransactions") # requires character_id and the user_id
def importtransactions(character_id, user_id):
    required_scopes = ['esi-wallet.read_character_wallet.v1']
    token = Token.get_token(character_id, required_scopes)
    user = User.objects.get(id=user_id)
    character = Character.objects.filter(character_id=character_id).first()
    if character.corporation_id is None:
        updatecharactermeta()
        character = Character.objects.filter(character_id=character_id).first()
    if (token is not None) and (token is not False):
        transresults = esi.client.Wallet.get_characters_character_id_wallet_transactions(
            # required parameter for endpoint
            character_id = character_id,
            # provide a valid access token, which wil be refresh the token if required
            token = token.valid_access_token()
        ).results()
        # Let's also get the last transaction from the user..
        try:
            lasttran = Transaction.objects.filter(user_id=user_id,character_id=character_id,is_personal__isnull=False).latest('transaction_id')
            lasttran = lasttran.transaction_id
        except:
            lasttran = 0
        # Last transaction id got, let's start iterating yo
        bulk_mgr = BulkCreateManager(chunk_size=100)
        for trans in transresults:
            if (trans.get('transaction_id') > lasttran) and (trans.get('is_personal') is True):
                print(trans.get('transaction_id'))
                #we add here
                bulk_mgr.add(
                    Transaction.objects.create(
                    client_id=trans.get('client_id'),
                    date=trans.get('date'),
                    is_buy=trans.get('is_buy'),
                    is_personal=trans.get('is_personal'),
                    journal_ref_id=trans.get('journal_ref_id'),
                    location_id=trans.get('location_id'),
                    quantity=trans.get('quantity'),
                    transaction_id=trans.get('transaction_id'),
                    type_id=trans.get('type_id'),
                    unit_price=trans.get('unit_price'),
                    character_id=character_id,
                    user=user,
                    ))
            else:
                #We've reached the breaking point, aka we are up to date..
                pass

        bulk_mgr.done()

    # Let's also see if there's a corp transaction endpoint
    # Clear old variables
    token = None
    required_scopes = None
    bulk_mgr = None
    lasttran = None

    required_scopes = ['esi-wallet.read_corporation_wallets.v1']
    token = Token.get_token(character_id, required_scopes)
    if (token is not None) and (token is not False):
        division = 1
        bulk_mgr = BulkCreateManager(chunk_size=100)
        try:
            lasttran = Transaction.objects.filter(user_id=user_id,corporation_id=character.corporation_id).latest('transaction_id')
            lasttran = lasttran.transaction_id
        except:
            lasttran = 0
        while division < 8:
            transresults = esi.client.Wallet.get_corporations_corporation_id_wallets_division_transactions(
                # required parameter for endpoint
                corporation_id = character.corporation_id,
                division = division,
                # provide a valid access token, which wil be refresh the token if required
                token = token.valid_access_token()
            ).results()
            division = division + 1
            for trans in transresults:
                if (trans.get('transaction_id') > lasttran) and (trans.get('is_personal') is not True) and (trans.get('is_personal') is None):
                    #we add here
                    bulk_mgr.add(Transaction(
                        client_id=trans.get('client_id'),
                        date=trans.get('date'),
                        is_buy=trans.get('is_buy'),
                        is_personal=trans.get('is_personal'),
                        journal_ref_id=trans.get('journal_ref_id'),
                        location_id=trans.get('location_id'),
                        quantity=trans.get('quantity'),
                        transaction_id=trans.get('transaction_id'),
                        type_id=trans.get('type_id'),
                        unit_price=trans.get('unit_price'),
                        character_id=character_id,
                        corporation_id=character.corporation_id,
                        user=user,
                        ))
                else:
                    #We've reached the breaking point, aka we are up to date..
                    pass
        bulk_mgr.done()
    return character_id
    #maybe we add the next task (aka processing, or flag the user for processing..)

@shared_task(name="importorders") # requires character_id and the user_id
def importorders(character_id, user_id):
    required_scopes = ['esi-markets.read_character_orders.v1']
    token = Token.get_token(character_id, required_scopes)
    user = User.objects.get(id=user_id)
    character = Character.objects.filter(character_id=character_id).first()
    if character.corporation_id is None:
        updatecharactermeta()
        character = Character.objects.filter(character_id=character_id).first()
    if (token is not None) and (token is not False): 
        ordresults = esi.client.Market.get_characters_character_id_orders(
            # required parameter for endpoint
            character_id = character_id,
            # provide a valid access token, which wil be refresh the token if required
            token = token.valid_access_token()
        ).results()
        # Let's also get the last transaction from the user..
        try:
            lastord = Order.objects.filter(user_id=user_id,character_id=character_id,is_corporation=0).latest('order_id')
            lastord = lastord.order_id
        except:
            lastord = 0
        try:
            currentorders = Order.objects.filter(user_id=user_id,character_id=character_id,is_corporation=0,state="Open").values('order_id')
            currentorders = [pullme.get('order_id') for pullme in currentorders]
        except:
            currentorders = []
        # Last transaction id got, let's start iterating yo
        bulk_mgr = BulkCreateManager(chunk_size=100)
        for ord in ordresults:
            #let's pluck the order from the currentorders list
            try:
                currentorders.remove(ord.get('order_id'))
            except:
                pass
            if (ord.get('order_id') > lastord) and (ord.get('is_corporation') is not True):
                #It's a new order..
                bulk_mgr.add(Order(
                    duration=ord.get('duration'),
                    is_buy_order=ord.get('is_buy_order'),
                    is_corporation=False,
                    issued=ord.get('issued'),
                    location_id=ord.get('location_id'),
                    min_volume=ord.get('min_volume'),
                    order_id=ord.get('order_id'),
                    price=ord.get('price'),
                    range=ord.get('range'),
                    character_id=character_id,
                    last_updated=timezone.now(),
                    region_id=ord.get('region_id'),
                    type_id=ord.get('type_id'),
                    volume_remain=ord.get('volume_remain'),
                    volume_total=ord.get('volume_total'),
                    user=user,
                    ))
            else:
                # It's an order we probably gotta update!
                try:
                    Order.objects.filter(order_id=ord.get('order_id')).update(
                        volume_remain=ord.get('volume_remain'),
                        price=ord.get('price'),
                        duration=ord.get('duration'),
                        last_updated=timezone.now(),
                        )
                except:
                    pass
        bulk_mgr.done()
        # Okay we have a list of orders in database that aren't there anymore.. Let's go back and get history and check what we got
        orderhistory = esi.client.Market.get_characters_character_id_orders_history(
            # required parameter for endpoint
            character_id = character_id,
            # provide a valid access token, which wil be refresh the token if required
            token = token.valid_access_token()
        ).results()
        for oldorder in currentorders:
            foo = True
            # We're gonna compare with the history
            lookup = first(x for x in orderhistory if x.get('order_id') == oldorder)
            if lookup is not None:
                #we found the old order in history! Let's update
                Order.objects.filter(order_id=lookup.get('order_id')).update(
                        volume_remain=lookup.get('volume_remain'),
                        price=lookup.get('price'),
                        duration=lookup.get('duration'),
                        state=lookup.get('state'),
                        last_updated=timezone.now(),
                        )
                updateord = Order.objects.filter(order_id=lookup.get('order_id')).first()
                notify.send(character, recipient=user, verb=f"Order has been {lookup.get('state')}",action_object=updateord)
                #signal fire notification

    #Okay, let's get corp tokens now
    required_scopes = ['esi-markets.read_corporation_orders.v1']
    token = Token.get_token(character_id, required_scopes)
    if (token is not None) and (token is not False):        
        ordresults = esi.client.Market.get_corporations_corporation_id_orders(
            # required parameter for endpoint
            corporation_id = character.corporation_id,
            # provide a valid access token, which wil be refresh the token if required
            token = token.valid_access_token()
        ).results()
        # Let's also get the last transaction from the user..
        try:
            lastord = Order.objects.filter(user_id=user_id,corporation_id=character.corporation_id,is_corporation=1).latest('order_id')
            lastord = lastord.order_id
        except:
            lastord = 0
        try:
            currentorders = Order.objects.filter(user_id=user_id,corporation_id=character.corporation_id,is_corporation=1,state="Open").values('order_id')
            currentorders = [pullme.get('order_id') for pullme in currentorders]
        except:
            currentorders = []
        # Last transaction id got, let's start iterating yo
        bulk_mgr = BulkCreateManager(chunk_size=100)
        for ord in ordresults:
            #let's pluck the order from the currentorders list
            try:
                currentorders.remove(ord.get('order_id'))
            except:
                pass
            if (ord.get('order_id') > lastord):
                #It's a new order..
                bulk_mgr.add(Order(
                    duration=ord.get('duration'),
                    is_buy_order=ord.get('is_buy_order'),
                    is_corporation=True,
                    issued=ord.get('issued'),
                    location_id=ord.get('location_id'),
                    min_volume=ord.get('min_volume'),
                    order_id=ord.get('order_id'),
                    price=ord.get('price'),
                    range=ord.get('range'),
                    character_id=character_id,
                    corporation_id=character.corporation_id,
                    last_updated=timezone.now(),
                    region_id=ord.get('region_id'),
                    type_id=ord.get('type_id'),
                    volume_remain=ord.get('volume_remain'),
                    volume_total=ord.get('volume_total'),
                    user=user,
                    ))
            else:
                # It's an order we probably gotta update!
                try:
                    Order.objects.filter(order_id=ord.get('order_id')).update(
                        volume_remain=ord.get('volume_remain'),
                        price=ord.get('price'),
                        duration=ord.get('duration'),
                        last_updated=timezone.now(),
                        )
                except:
                    pass
        bulk_mgr.done()
        # Okay we have a list of orders in database that aren't there anymore.. Let's go back and get history and check what we got
        orderhistory = esi.client.Market.get_corporations_corporation_id_orders_history(
            # required parameter for endpoint
            corporation_id = character.corporation_id,
            # provide a valid access token, which wil be refresh the token if required
            token = token.valid_access_token()
        ).results()
        for oldorder in currentorders:
            foo = True
            # We're gonna compare with the history
            lookup = first(x for x in orderhistory if x.get('order_id') == oldorder)
            if lookup is not None:
                #we found the old order in history! Let's update
                Order.objects.filter(order_id=lookup.get('order_id')).update(
                        volume_remain=lookup.get('volume_remain'),
                        price=lookup.get('price'),
                        duration=lookup.get('duration'),
                        state=lookup.get('state'),
                        last_updated=timezone.now(),
                        )
                updateord = Order.objects.filter(order_id=lookup.get('order_id')).first()
                notify.send(character, recipient=user, verb=f"Order has been {lookup.get('state')}",action_object=updateord)
                #signal fire notification

    return character_id
    #maybe we add the next task (aka processing, or flag the user for processing..)

@shared_task(name="pullusercharacters") # requires a user_id
def pullusercharacters(user_id):
    # let's first get user's characters
    tokenchars = []
    tokenlist = Token.objects.filter(user=user_id).values('character_id')
    user = User.objects.get(id=user_id)
    for toke in tokenlist:
        #let's also add the user's character to the database
        character_id = toke.get('character_id')
        char = Character.objects.get_or_create(character_id = character_id,user = user)
    #Okay, we've update the user's character list.. Let's get some characters that need updating!
    topull = Character.objects.filter(user=user_id,last_esi_pull__lt=one_hour_ago()).values('character_id') #will eventually add some filtering for last_esi_pull
    if len(topull) < 1:
        return True
    try:
        pullthis = [pullme.get('character_id') for pullme in topull]
        for char in pullthis:
            importtransactions.delay(char, user_id)
            importorders.delay(char,user_id)
            #Let's also update the character
            Character.objects.filter(character_id=char).update(last_esi_pull=timezone.now())
    except:
        return True
    return character_id
    #maybe we add the next task (aka processing, or flag the user for processing..)

@shared_task(name="pullusers") # requires a user_id
def pullusers():
    # let's first get user's characters
    userlist = User.objects.all()
    for getuser in userlist:
        pullusercharacters.delay(getuser.id)
        getstockfromtransactions.delay(getuser.id)
    return True

@shared_task(name="updatecharactermeta") # requires a user_id
def updatecharactermeta():
    try:
        charlist = Character.objects.filter(corporation_id__isnull=True)
    except:
        charlist = []
    for char in charlist:
        #iterate the characters and get public data
        try:
            chardata = esi.client.Character.get_characters_character_id(character_id = char.character_id).results()
            #data got, let's update the database
            char.alliance_id = chardata.get('alliance_id')
            char.corporation_id = chardata.get('corporation_id')
            char.name = chardata.get('name')
            char.save()
        except:
            pass
        
@shared_task(name="updatetransactionmeta") # requires a user_id
def updatetransactionmeta():
    try:
        translist = Transaction.objects.filter(type_name="Unknown")
    except:
        translist = []
    for tran in translist:
        #iterate the characters and get public data
        try:
            #let's go through and try to find the type/system
            if tran.location_id < 70000000:
                station, bleh = EveStation.objects.get_or_create_esi(id=tran.location_id)
            else:
                station = Structure.objects.filter(id=tran.location_id).first()
                if station is None:
                    # we gotta get the station.. let's find a token and grab it
                    required_scopes = ['esi-universe.read_structures.v1']
                    token = Token.get_token(tran.character_id, required_scopes)
                    user = User.objects.get(id=tran.user_id)
                    try:
                        stationdata = esi.client.Universe.get_universe_structures_structure_id(structure_id = tran.location_id,token = token.valid_access_token()).results()
                        Structure.objects.create(id=tran.location_id,solar_system_id = stationdata.get('solar_system_id'),name = stationdata.get('name'),owner_id = stationdata.get('owner_id'),position_x = stationdata.get('position').get('x'),position_y = stationdata.get('position').get('y'),position_z = stationdata.get('position').get('z'),type_id = stationdata.get('type_id'))
                        station = Structure.objects.filter(id=tran.location_id).first()
                    except:
                        pass
                else:
                    pass
            #okay let's get the typeid
            try:
                item, trash = EveType.objects.get_or_create_esi(id=tran.type_id)
                tran.station_name = station.name
                tran.type_name = item.name
                tran.save()
            except:
                pass
        except:
            pass

@shared_task(name="getstockfromtransactions") # requires a user_id
def getstockfromtransactions(user_id):
    user = User.objects.get(id=user_id)
    characters = Character.objects.filter(user=user)
    try:
        translist = Transaction.objects.filter(user=user,is_buy=1,processed=0)
    except:
        translist = []
    bulk_mgr = BulkCreateManager(chunk_size=100)
    for tran in translist:
        #iterate the characters and get public data
        try:
            # Let's get the character
            lookup = first(x for x in characters if x.character_id == tran.character_id)
            item, trash = EveType.objects.get_or_create_esi(id=tran.type_id)
            buybroker = lookup.preferences['trade__buy_broker']
            #Okay, we got the transaction, the tax data.. Let's start adding stock
            tranamount = tran.quantity * tran.unit_price
            taxes = tranamount * buybroker
            tax_data = {'buy_broker': buybroker}
            tax_data = json.dumps(tax_data)
            bulk_mgr.add(Stock(
                user = user,
                transaction = tran,
                item = item,
                amount = tran.unit_price,
                date= tran.date,
                quantity = tran.quantity,
                station = tran.location_id,
                taxes = taxes,
                unit_tax = taxes / tran.quantity,
                tax_data = tax_data
                ))
            # Let's also mark transaction as processed
            tran.processed = True
            tran.save()
        except:
            pass

    bulk_mgr.done()
    #getprofitfromtransactions.delay(user_id)

@shared_task(name="getprofitfromtransactions") # requires a user_id
def getprofitfromtransactions(user_id):
    user = User.objects.get(id=user_id)
    characters = Character.objects.filter(user=user)
    try:
        translist = Transaction.objects.filter(user=user,is_buy=0,processed=0).order_by('-date')
    except:
        translist = []
    bulk_mgr = BulkCreateManager(chunk_size=100)
    for tran in translist:
        #iterate the characters and get public data
        # Let's get the character
        lookup = first(x for x in characters if x.character_id == tran.character_id)
        item, trash = EveType.objects.get_or_create_esi(id=tran.type_id)
        charsellbroker = lookup.preferences['trade__sell_broker']
        charsalestax = lookup.preferences['trade__sales_tax']
        #Okay, we got the transaction, the tax data.. Let's start by finding some stock
        quantity_to_process = tran.quantity
        total_profit = Decimal(0)
        totaltax = Decimal(0)
        while quantity_to_process > 0:
            try:
                foundstock = Stock.objects.filter(user=user,item=item).order_by('date').first()
            except:
                # No stock found, if the transaction is older than 6h let's go ahead and set the transaction processed
                tran.processed = True
                tran.save()
                quantity_to_process = 0
                continue
            #We have stock, let's do some thinking
            try:
                if (foundstock is not None)  and (foundstock.quantity > quantity_to_process):
                    current_quant_process = quantity_to_process
                    #we found enough stock, hell yeah. It's not == so we can deduct and save the stock
                    foundstock.quantity = foundstock.quantity - current_quant_process
                    foundstock.save()

                    #okay, stock data is updated, let's do some maths to calculate profit
                    #First the sales tax
                    sales_tax = (tran.unit_price * current_quant_process) * charsalestax
                    broker_fee = (tran.unit_price * current_quant_process) * charsellbroker
                    tax_data = {'sell_broker': charsellbroker,'sales_tax': charsalestax}
                    tax_data = json.dumps(tax_data)
                    totaltax = sales_tax + broker_fee
                    unit_tax = totaltax / current_quant_process
                    # Okay we have the selling taxes calculated, let's do the math on the stock
                    stock_price = foundstock.amount
                    stock_unit_tax = foundstock.unit_tax
                    stock_total_tax = stock_unit_tax * current_quant_process
                    totaltax = totaltax + stock_total_tax
                    #Total tax calculated, let's check the gross margin
                    price_spread = tran.unit_price - foundstock.amount
                    total_spread = price_spread * current_quant_process
                    total_net = total_spread - totaltax
                    total_profit = total_profit + total_net

                    stock_data = model_to_dict(foundstock)
                    stock_data = json.dumps(stock_data)

                    #Okay, we should have all the math done.. Let's add a profit row
                    bulk_mgr.add(Profit(
                        user = user,
                        transaction = tran,
                        item = item,
                        stock_data = stock_data,
                        amount = total_net,
                        quantity = current_quant_process,
                        station = tran.location_id,
                        taxes = totaltax,
                        #unit_tax = totaltax / current_quant_process,
                        tax_data = tax_data,
                        ))
                    quantity_to_process = quantity_to_process - current_quant_process
                elif (foundstock is not None) and (foundstock.quantity == quantity_to_process):
                    current_quant_process = quantity_to_process
                    #we found enough stock, hell yeah. This time it IS exact so we can delete
                    stock_data = model_to_dict(foundstock)
                    stock_data = json.dumps(stock_data)
                    foundstock.delete()

                    #okay, stock data is updated, let's do some maths to calculate profit
                    #First the sales tax
                    sales_tax = (tran.unit_price * current_quant_process) * charsalestax
                    broker_fee = (tran.unit_price * current_quant_process) * charsellbroker
                    tax_data = {'sell_broker': charsellbroker,'sales_tax': charsalestax}
                    tax_data = json.dumps(tax_data)
                    totaltax = sales_tax + broker_fee
                    unit_tax = totaltax / current_quant_process
                    # Okay we have the selling taxes calculated, let's do the math on the stock
                    stock_price = foundstock.amount
                    stock_unit_tax = foundstock.unit_tax
                    stock_total_tax = stock_unit_tax * current_quant_process
                    totaltax = totaltax + stock_total_tax
                    #Total tax calculated, let's check the gross margin
                    price_spread = tran.unit_price - foundstock.amount
                    total_spread = price_spread * current_quant_process
                    total_net = total_spread - totaltax
                    total_profit = total_profit + total_net

                    #Okay, we should have all the math done.. Let's add a profit row
                    bulk_mgr.add(Profit(
                        user = user,
                        transaction = tran,
                        item = item,
                        stock_data = stock_data,
                        amount = total_net,
                        quantity = current_quant_process,
                        station = tran.location_id,
                        taxes = totaltax,
                        #unit_tax = totaltax / current_quant_process,
                        tax_data = tax_data,
                        ))
                    quantity_to_process = quantity_to_process - current_quant_process
                elif (foundstock is not None) and (foundstock.quantity < quantity_to_process):
                    current_quant_process = foundstock.quantity
                    #we found some stock, but it's not enough to satisfy the sell transaction. We can still delete the stock though!
                    stock_data = model_to_dict(foundstock)
                    stock_data = json.dumps(stock_data)
                    foundstock.delete()

                    #okay, stock data is updated, let's do some maths to calculate profit
                    #First the sales tax
                    sales_tax = (tran.unit_price * current_quant_process) * charsalestax
                    broker_fee = (tran.unit_price * current_quant_process) * charsellbroker
                    tax_data = {'sell_broker': charsellbroker,'sales_tax': charsalestax}
                    tax_data = json.dumps(tax_data)
                    totaltax = sales_tax + broker_fee
                    unit_tax = totaltax / current_quant_process
                    # Okay we have the selling taxes calculated, let's do the math on the stock
                    stock_price = foundstock.amount
                    stock_unit_tax = foundstock.unit_tax
                    stock_total_tax = stock_unit_tax * current_quant_process
                    totaltax = totaltax + stock_total_tax
                    #Total tax calculated, let's check the gross margin
                    price_spread = tran.unit_price - foundstock.amount
                    total_spread = price_spread * current_quant_process
                    total_net = total_spread - totaltax
                    total_profit = total_profit + total_net

                    #Okay, we should have all the math done.. Let's add a profit row
                    bulk_mgr.add(Profit(
                        user = user,
                        transaction = tran,
                        item = item,
                        stock_data = stock_data,
                        amount = total_net,
                        quantity = current_quant_process,
                        station = tran.location_id,
                        taxes = totaltax,
                        unit_tax = totaltax / current_quant_process,
                        tax_data = tax_data,
                        ))
                    quantity_to_process = quantity_to_process - current_quant_process
                else:
                    quantity_to_process = 0
                    continue
            except:
                pass

        # Let's also mark transaction as processed
        tran.profit = total_profit
        tran.taxes = totaltax
        if total_profit > 0:
            tran.margin = total_profit / ((tran.unit_price * tran.quantity) - total_profit - totaltax)
        tran.processed = True
        tran.save()
    bulk_mgr.done()
