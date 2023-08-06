from logging import getLogger
from time import time

from pyinaturalist_convert.fts import TaxonAutocompleter, load_fts_taxa
from test.conftest import SAMPLE_DATA_DIR

CSV_DIR = SAMPLE_DATA_DIR / 'inaturalist-taxonomy.dwca'
COUNTS_PATH = SAMPLE_DATA_DIR / 'taxon_counts_fts.parquet'
logger = getLogger(__name__)


def test_text_search(tmp_path):
    db_path = tmp_path / 'taxa.db'
    load_fts_taxa(csv_dir=CSV_DIR, db_path=db_path, counts_path=COUNTS_PATH)
    ta = TaxonAutocompleter(db_path=db_path)

    results = ta.search('ave')
    assert results[0].id == 3 and results[0].name == 'Aves'

    results = ta.search('franco')
    assert len(results) == 3
    assert results[0].id == 649 and results[0].name == 'Black Francolin'


def benchmark():
    iterations = 10000
    ta = TaxonAutocompleter()
    start = time()

    for _ in range(iterations):
        ta.search('berry', language=None)
    elapsed = time() - start

    logger.info(f'Total: {elapsed:.2f}s')
    logger.info(f'Avg per query: {(elapsed/iterations)*1000:2f}ms')
