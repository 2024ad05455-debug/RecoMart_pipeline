import json
from datetime import datetime
import os

BASE_PATH = EBITSDM4MLRecoMart_pipeline
META_PATH = os.path.join(BASE_PATH, data, metadata)

os.makedirs(META_PATH, exist_ok=True)

lineage = {
    pipeline RecoMart,
    stage feature_engineering,
    timestamp datetime.now().isoformat(),
    source_datasets [
        datarawcsvuser_events,
        datarawapiproduct_data
    ],
    processed_datasets [
        dataprocessedfeatures_v1
    ],
    transformations [
        ingestioningest_events.py,
        ingestioningest_products_api.py,
        featuresfeature_engineering.sql,
        featuresfeature_engineering.py
    ],
    feature_store [
        registryregister_features.py
    ],
    versioning {
        tool DVC,
        repo Git
    }
}

output_file = os.path.join(META_PATH, flineage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json)

with open(output_file, w) as f
    json.dump(lineage, f, indent=4)

print(fLineage file created {output_file})
