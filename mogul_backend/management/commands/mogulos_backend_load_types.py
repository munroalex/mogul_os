import logging
from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...constants import (
    EVE_CATEGORY_ID_STATION,
    EVE_CATEGORY_ID_SHIP,
    EVE_CATEGORY_ID_MODULE,
    EVE_CATEGORY_ID_CHARGE,
    EVE_CATEGORY_ID_BLUEPRINT,
    EVE_CATEGORY_ID_SKILL,
    EVE_CATEGORY_ID_DRONE,
    EVE_CATEGORY_ID_IMPLANT,
    EVE_CATEGORY_ID_FIGHTER,
    EVE_CATEGORY_ID_STRUCTURE,
    EVE_CATEGORY_ID_MATERIAL,
    EVE_CATEGORY_ID_ACCESSORIES,
    EVE_CATEGORY_ID_TRADING,
    EVE_CATEGORY_ID_COMMODITY,
    EVE_CATEGORY_ID_DEPLOYABLE,
    EVE_CATEGORY_ID_STARBASE,
    EVE_CATEGORY_ID_REACTION,
    EVE_CATEGORY_ID_ASTEROID,
    EVE_CATEGORY_ID_APPAREL,
    EVE_CATEGORY_ID_SUBSYSTEM,
    EVE_CATEGORY_ID_RELICS,
    EVE_CATEGORY_ID_DECRYPTORS,
    EVE_CATEGORY_ID_IHUBUPGRADES,
    EVE_CATEGORY_ID_SOVSTRUCTURES,
    EVE_CATEGORY_ID_PLANETIND,
    EVE_CATEGORY_ID_PLANETRESOURCE,
    EVE_CATEGORY_ID_PLANETCOMMODITIES,
    EVE_CATEGORY_ID_ORBITALS,
    EVE_CATEGORY_ID_STRUCTUREMODULE,
    EVE_CATEGORY_ID_PLACEABLE,
    EVE_CATEGORY_ID_SKINS
)

class Command(BaseCommand):
    help = "Preloads data required for this app from ESI"

    def handle(self, *args, **options):
        call_command(
            "eveuniverse_load_types",
            "MogulOS",
            "--category_id",str(EVE_CATEGORY_ID_BLUEPRINT),
            "--category_id",str(EVE_CATEGORY_ID_SHIP),
            "--category_id",str(EVE_CATEGORY_ID_MODULE),
            "--category_id",str(EVE_CATEGORY_ID_CHARGE),
            "--category_id",str(EVE_CATEGORY_ID_SKILL),
            "--category_id",str(EVE_CATEGORY_ID_DRONE),
            "--category_id_with_dogma",str(EVE_CATEGORY_ID_IMPLANT),
            "--category_id",str(EVE_CATEGORY_ID_FIGHTER),
            "--category_id",str(EVE_CATEGORY_ID_STRUCTURE),
            "--category_id",str(EVE_CATEGORY_ID_MATERIAL),
            "--category_id",str(EVE_CATEGORY_ID_ACCESSORIES),
            "--category_id",str(EVE_CATEGORY_ID_TRADING),
            "--category_id",str(EVE_CATEGORY_ID_COMMODITY),
            "--category_id",str(EVE_CATEGORY_ID_DEPLOYABLE),
            "--category_id",str(EVE_CATEGORY_ID_STARBASE),
            "--category_id",str(EVE_CATEGORY_ID_REACTION),
            "--category_id",str(EVE_CATEGORY_ID_ASTEROID),
            "--category_id",str(EVE_CATEGORY_ID_APPAREL),
            "--category_id",str(EVE_CATEGORY_ID_SUBSYSTEM),
            "--category_id",str(EVE_CATEGORY_ID_RELICS),
            "--category_id",str(EVE_CATEGORY_ID_DECRYPTORS),
            "--category_id",str(EVE_CATEGORY_ID_IHUBUPGRADES),
            "--category_id",str(EVE_CATEGORY_ID_SOVSTRUCTURES),
            "--category_id",str(EVE_CATEGORY_ID_PLANETIND),
            "--category_id",str(EVE_CATEGORY_ID_PLANETRESOURCE),
            "--category_id",str(EVE_CATEGORY_ID_PLANETCOMMODITIES),
            "--category_id",str(EVE_CATEGORY_ID_ORBITALS),
            "--category_id",str(EVE_CATEGORY_ID_STRUCTUREMODULE),
            "--category_id",str(EVE_CATEGORY_ID_PLACEABLE),
            "--category_id",str(EVE_CATEGORY_ID_SKINS)
        )
