from box import Box
import itertools
from typing import List
from pyspark.sql import types as t, functions as f
from pyspark.sql import DataFrame
from featurestorebundle.feature.FeatureStore import FeatureStore
from featurestorebundle.entity.EntityGetter import EntityGetter


class MetadataJsonGetter:
    def __init__(self, feature_store: FeatureStore, entity_getter: EntityGetter, general_mapping: Box, category_mapping: Box) -> None:
        self.__feature_store = feature_store
        self.__category_mapping = dict(
            itertools.chain(
                *[list(itertools.product(value, [key])) for key, value in zip(category_mapping.keys(), category_mapping.values())]
            )
        )
        self.__general_mapping = general_mapping
        self.__entity = entity_getter.get()

    def __get_metadata_with_subcategory(self):
        metadata = self.__feature_store.get_metadata(entity_name=self.__entity.name)

        return (
            metadata.filter(f.col("entity") == self.__entity.name)
            .withColumn("subcategory", f.col("category"))
            .replace(to_replace=self.__category_mapping, subset=["category"])
        )

    def __rename_metadata(self, df: DataFrame, row: t.Row, general_mapping_dict: dict) -> dict:
        result = {
            (general_mapping_dict[col] if col in general_mapping_dict else col): (str(row[col]) if row[col] is not None else "")
            for col in df.columns
        }
        result["description"] = ""

        return result

    def get_jsons(self) -> List[dict]:
        metadata_with_subcategory = self.__get_metadata_with_subcategory()

        collected_data = metadata_with_subcategory.collect()
        category_list = [row.category for row in (metadata_with_subcategory.select("category").distinct().collect())]
        all_categories = []
        for category in category_list:
            category_dict = {
                "title": category,
                "category": category,
                "subcategory": "",
                "author": "PX",
            }

            items = []
            for row in collected_data:
                if row["category"] == category:
                    items.append(self.__rename_metadata(metadata_with_subcategory, row, self.__general_mapping.to_dict()))
                    category_dict["items"] = items

            all_categories.append(category_dict)

        return all_categories
