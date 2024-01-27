import os
import json
from PIL import Image, ImageEnhance, ImageChops

path = 'C:\\Users\\sd3c2\\AppData\\Roaming\\.minecraft\\resourcepacks\\Space\\assets\\minecraft'
modelsPath = path + "\\models\\custom"
modelsMiscPath = path + "\\models"
texturesPath = path + "\\textures\\item"

for fileName in os.listdir(modelsPath):
    if not fileName.endswith(".json"): continue
    if fileName.endswith("_hurt.json"): continue

    hurtFileName = modelsPath + '\\' + fileName[:-5] + "_hurt.json"
    with open(modelsPath + '\\' + fileName, 'r+') as f:
        data = json.load(f)
        data["textures"]["0"] += "_hurt"
        with open(hurtFileName, 'w') as f_hurt:
            f_hurt.seek(0)
            json.dump(data, f_hurt, indent=4)
            f_hurt.truncate()

    print(f"Created hurt json for: {fileName}.")

redness = 0.4

for fileName in os.listdir(texturesPath):
    if not fileName.endswith(".png"): continue
    if fileName.endswith("_hurt.png"): continue

    hurtFileName = texturesPath + '\\' + fileName[:-4] + "_hurt.png"

    img = Image.open(texturesPath + '\\' + fileName).convert('RGBA')
    redOverlay = Image.new('RGBA', img.size, (255, 0, 0, int(255 * redness)))
    hurtImg = Image.alpha_composite(img.convert('RGBA'), redOverlay)
    hurtImg.save(hurtFileName)

    print(f"Created hurt image for: {fileName}")

diamond_sword = modelsMiscPath + "\\item\\diamond_sword.json"

with open(diamond_sword, 'r') as f:
    data = json.load(f)

    new_overrides = []
    existing_models = {override["model"] for override in data["overrides"]}

    for index, override in enumerate(data["overrides"]):
        new_model = override["model"] + "_hurt"
        if not new_model in existing_models:
            if not override["model"].endswith("_hurt"):
                new_custom_model_data = 10000000 + index + 1
                new_override = {"predicate": {"custom_model_data": new_custom_model_data}, "model": new_model}
                new_overrides.append(new_override)

    data["overrides"].extend(new_overrides)

with open(diamond_sword, 'w') as f:
    json.dump(data, f, indent=4)