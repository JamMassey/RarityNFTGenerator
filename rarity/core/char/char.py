import json
import os

from core.roll import lucky_item_pool_roll
from core.util import overlay
from PIL import Image


class CharacterGenerator:
    def __init__(self, json_path):
        with open(json_path, "r") as f:
            gen_data = json.load(f)
        self.gen_data = gen_data
        self.last_generated_image_metadata = {}

    def handle_layer(self, ele):
        cumalitive_probability = 1.0
        while ele["Type"] != "Category":
            roll = lucky_item_pool_roll(float(ele["Chance"]), ele["SubCategories"], ele["CategoryProbabilities"])
            if roll == "":
                instance_probability = 1 - float(ele["Chance"])
                cumalitive_probability = cumalitive_probability * instance_probability
                print(
                    "Missed Subcategory Roll on Category: {}. Instance Chance: {} Cumalitive Chance: {}".format(
                        ele["Name"], str(round(instance_probability, 5) * 100) + "%", str(round(cumalitive_probability, 5) * 100) + "%"
                    )
                )
                return ""
            instance_probability = roll[1] * float(ele["Chance"])
            cumalitive_probability = cumalitive_probability * instance_probability
            print(
                "Rolled Subcategory: {} in Category: {}. Instance Chance: {} Cumalitive chance: {}".format(
                    roll[0]["Name"],
                    ele["Name"],
                    str(round(instance_probability, 5) * 100) + "%",
                    str(round(cumalitive_probability, 5) * 100) + "%",
                )
            )
            ele = roll[0]

        if ele["Type"] == "Category":
            assets_path = ele["Path"]
            roll = lucky_item_pool_roll(float(ele["Chance"]), os.listdir(assets_path), ele["AssetProbabilities"])
            if roll == "":
                instance_probability = 1 - float(ele["Chance"])
                cumalitive_probability = cumalitive_probability * instance_probability
                print(
                    "Missed Roll on Category: {}. Instance Chance: {} Cumalitive Chance: {}".format(
                        ele["Name"], str(round(instance_probability, 5) * 100) + "%", str(round(cumalitive_probability, 5) * 100) + "%"
                    )
                )
                return ""
            asset_loc = assets_path + "/" + roll[0]
            instance_probability = roll[1] * float(ele["Chance"])
            cumalitive_probability = cumalitive_probability * instance_probability
            print(
                "Rolled Asset: {} in Category: {}. Instance Chance: {} Cumalitive chance: {}".format(
                    roll[0], ele["Name"], str(round(instance_probability, 5) * 100) + "%", str(round(cumalitive_probability, 5) * 100) + "%"
                )
            )
            self.last_generated_image_metadata[ele["Name"]] = asset_loc

    def generate_visual_attributes(self, dimensions=[32, 32]):
        self.last_generated_image_metadata = {}
        for attribute, value in self.gen_data.items():
            self.handle_layer(value)
        return self.last_generated_image_metadata

    def generate_image(self, metadata={}):
        if metadata == {}:
            metadata = self.generate_visual_attributes()
        image = Image.new("RGBA", (32, 32))
        for key, value in metadata.items():
            image = overlay(image, Image.open(value))
        return image
