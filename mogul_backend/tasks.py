# Create your tasks here

from celery import shared_task
from eveuniverse.models import EveType, EveRace


@shared_task(name="createitemdatabase")
def createitemdatabase():
    EveRace.objects.update_or_create_all_esi()
    EveType.objects.update_or_create_all_esi()
    return "Okay"

@shared_task(name="importtransactions")
def importtransactions(character_id):
    required_scopes = ['esi-wallet.read_character_wallet.v1']
    token = Token.get_token(character_id, required_scopes)
    try:
        result = esi.client.Wallet.get_characters_character_id_wallet_transactions(
            # required parameter for endpoint
            character_id = character_id,
            # provide a valid access token, which wil be refresh the token if required
            token = token.valid_access_token()
        ).results()
    except HTTPNotFound:
            print("error getting transactions")
    # We've got data, lets add it to the database now
    print(character_id)
    return character_id
