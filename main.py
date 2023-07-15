from loaders.abn_amro.main import load_abn_amro
from loaders.rabobank.main import load_rabobank
from enrich.categories import enrich_with_categories
from enrich.fixed import enrich_with_fixed
from enrich.party import enrich_with_clean_party
from insert.expenses import import_expenses
from insert.inflation import import_inflation

load_abn_amro()
load_rabobank()

enrich_with_fixed()
enrich_with_clean_party()
enrich_with_categories()

import_expenses()
import_inflation()