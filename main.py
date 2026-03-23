import UnityPy
from PIL import Image
import os
from pathlib import Path
import re
import math
import json
from argparse import ArgumentParser

input_root = "AssetBundles"
output_root = "Output"

# (optional) Path of the base game AssetBundles - to get missing painting & paintingface files
# You can copy the game folder or download it with https://github.com/nobbyfix/AzurLane-AssetDownloader
# e.g: r'C:\....\....\MuMuSharedFolder\AzurLane_backup_data\AssetBundles'
asset_warehouse_path = r""

asset_group_path = None
saveMesh = False

# face offset, I think most of these also exist in the game, only test on CN assets (iOS: $paintinghash$594$3797e24395a3763b)
face_fix = {
    "longxiang_3": [-1, 0, -1, 0],
    "u110_6_n": [0, -1, 0, -1],
    "hamanii": [0, 0, 0, 0],
    "xia": [0, 0, 0, 0],
    "kelifulan_6_n": [0, -1, 0, -1],
    "baerdimo_6_n": [0, -1, 0, -1],
    "yalisangna_2_n": [0, -1, 0, -1],
    "yalisangna_2_n_hx": [0, -1, 0, -1],
    "xifujiniya": [0, 0, 0, 1],
    "qiye_8_n": [0, -1, 0, -1],
    "xiefeierde_3_n": [0, -1, 0, -1],
    "xiefeierde_4": [0, 0, 0, -1],
    "manchesite_3_n": [0, -1, 0, -1],
    "ouruola_3": [0, 0, -1, 0],
    "ouruola_h": [0, -1, 0, -1],
    "safuke": [0, 0, 0, -1],
    "safuke_hx": [0, 0, 0, -1],
    "yueke_h_n": [0, -1, 0, -1],
    "guanghui": [0, 0, -1, 0],
    "shengli": [0, -1, 0, -1],
    "chuixue_3": [0, 0, 0, 0],
    "shenxue_3_n": [0, -1, 0, -1],
    "xiao_4_n": [0, -1, 0, -1],
    "xiao_5_n": [0, -1, 0, -1],
    "jiahe_4_n": [0, -1, 0, -1],
    "dafeng_5": [-1, 0, -1, 0],
    "xipeierhaijunshangjiang_3_n": [0, -1, 0, -1],
    "ougen": [0, 0, 0, 0],
    "ougen_hx": [0, 0, 0, 0],
    "bisimai_h_n": [0, -5, 0, -5],
    "huonululu_5_n": [0, -1, 0, -1],
    "dachao_2": [0, 0, 1, 0],
    "lemaer_4_n": [0, -1, 0, -1],
    "mingniabolisi": [0, 0, 0, -1],
    "mingniabolisi_hx": [0, 0, 0, -1],
    "mingniabolisi_3": [-1, 0, -1, 0],
    "mingniabolisi_3_n": [-1, 0, -1, 0],
    "heizewude": [0, 0, 0, 0],
    "u73_4_n": [0, -1, 0, -1],
    "edu": [0, 0, 0, 0],
    "shuixingjinian_3_n": [0, -1, 0, -1],
    "qiabayefu_2": [0, 0, 0, -1],
    "qiabayefu_2_n": [0, 0, 0, -1],
    "linuo_5_n": [0, -1, 0, -1],
    "changbo_4_n": [0, -1, 0, -1],
    "wokelan_2_n": [0, -1, 0, -1],
    "hemin_4": [-1, 0, -1, 0],
    "xiongye_3_n": [0, -1, 0, -1],
    "wenqinzuojiaobeidi": [1, 0, 1, 0],
    "talin_2_n": [0, -1, 0, -1],
    "moermansike": [0, -1, 0, -1],
    "moermansike_n": [0, -1, 0, -1],
    "weineituo_hx": [0, 0, -1, 0],
    "weineituo_n_hx": [0, 0, -1, 0],
    "weineituo_wjz_hx": [0, 0, -1, 0],
    "tuolichaili_2_n": [0, -1, 0, -1],
    "tikangdeluojia_2": [0, -1, 0, -1],
    "tikangdeluojia_2_hx": [0, -1, 0, -1],
    "tikangdeluojia_2_n": [0, -1, 0, -1],
    "tikangdeluojia_2_n_hx": [0, -1, 0, -1],
    "jiujinshan_4_n": [0, -1, 0, -1],
    "boyixi_5_n": [0, -1, 0, -1],
    "kalvbudisi_3_n": [0, -1, 0, -1],
    "fuerjia_2_n": [0, -1, 0, -1],
    "yueke_ger_3_n": [0, -1, 0, -1],
    "texiusi_2_n": [0, 1, 0, -2],
    "xufulun_2_n": [0, -1, 0, -1],
    "xiusidunii_2_n": [0, -1, 0, -1],
    "jinluhao_2_n": [0, -1, 0, -1],
    "songdiao_2_n": [0, -1, 0, -1],
    "huanchang_2_n": [-1, 0, -1, 0],
    "jianwu_3_n": [0, -1, 0, -1],
    "bailong_2_n": [0, -1, 0, -1],
    "safuke_xinshou": [0, 0, 0, -1],
    "chicheng_alter": [0, 0, -1, 0],
    "chicheng_alter_n": [0, 0, -1, 0],
    "rightchicheng_alter": [0, 0, -1, 0],
    "rightchicheng_alter_n": [0, 0, -1, 0],
    "bulunnusi_3": [-1, 0, -1, 0],
    "bulunnusi_3_n": [-1, 0, -1, 0],
}


def get_id_dict():
    painting2id = {}
    if (
        os.path.exists("ship_skin_template.json")
        and os.path.exists("ship_data_group.json")
        and os.path.exists("secretary_special_ship.json")
    ):
        group2id = {}
        # Map group types to group IDs
        with open("ship_data_group.json", "r", encoding="utf8") as f1:
            group_map = json.load(f1)
        for key in group_map:
            group_type = group_map[key]["group_type"]
            group2id[group_type] = key

        # Load skin template
        with open("ship_skin_template.json", "r", encoding="utf8") as f2:
            skin_map = json.load(f2)

        # Helper to format the prefix as "groupid_shipname"
        def get_formatted_prefix(skin_id_str, group_id):
            # Transformation rule: change the last digit of the skin ID to 0
            # to find the "base" ship entry (e.g., 990003 -> 990000)
            base_key = skin_id_str[:-1] + "0"
            if base_key in skin_map:
                ship_name = skin_map[base_key].get("name", "")
                if ship_name:
                    # Remove illegal characters and replace spaces with underscores
                    clean_name = re.sub(r'[\\/*?:"<>|]', "", ship_name).replace(
                        " ", "_"
                    )
                    return f"{group_id}_{clean_name}"
            return str(group_id)

        # Process skin_map (Main pass)
        for key in dict(reversed(list(skin_map.items()))):
            painting_name = skin_map[key]["painting"].lower()
            ship_group = skin_map[key]["ship_group"]
            gid = group2id.get(ship_group)
            if gid:
                painting2id[painting_name] = get_formatted_prefix(key, gid)

        # Process skin_map (Fallback pass)
        for key in dict(reversed(list(skin_map.items()))):
            painting_name = skin_map[key]["painting"].lower()
            if painting2id.get(painting_name) is None:
                gid = str(skin_map[key]["ship_group"])
                painting2id[painting_name] = get_formatted_prefix(key, gid)

        # Process secretary_special_ship.json (Child ships/Special cases)
        with open("secretary_special_ship.json", "r", encoding="utf8") as f3:
            child_map = json.load(f3)
        for key in child_map:
            if key.isnumeric():
                child_data = child_map[key]
                child_painting = child_data.get("painting")
                if child_painting:
                    # Use the 'group' field as defined in secretary_special_ship
                    gid = str(child_data.get("group", "999999"))
                    # Map the painting (lowercase) to the base ship name prefix
                    painting2id[child_painting.lower()] = get_formatted_prefix(key, gid)

    return painting2id


def custom_round(n):
    floor_value = math.floor(n)
    decimal_part = n - floor_value
    if decimal_part == 0.5:
        return floor_value + 1
    else:
        return round(n)


def save_image(img, path_str, compress=False, use_webp=False):
    # Saves images as either optimized PNG or WebP.
    if use_webp:
        # quality=80-90 provides a great balance of size and visual fidelity
        img.save(path_str, format="WEBP", quality=85, lossless=False)
    elif compress:
        try:
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            # Quantize to 256 colors for PNG compression
            q_img = img.quantize(colors=256, method=Image.Quantize.MAXCOVERAGE)
            q_img.save(path_str, format="PNG", optimize=True, compress_level=9)
        except Exception as e:
            # Fallback to standard optimization if quantization fails
            img.save(path_str, format="PNG", optimize=True, compress_level=9)
    else:
        img.save(path_str, format="PNG")

    print(f"Saved: {os.path.basename(path_str)}")


def get_canvas(layer):
    texture = layer["texture"].image
    size = layer["size"]
    v_raw = []
    vt_raw = []
    for line in layer["mesh"].export().splitlines():
        if line.startswith("v "):
            vertex = line.split(" ")[1:]
            v_raw.append([int(n) for n in vertex])
        if line.startswith("vt "):
            vertex = line.split(" ")[1:]
            vt_raw.append([float(n) for n in vertex])
    assert len(v_raw) == len(
        vt_raw
    ), "Unequal number of mesh vertices to texture vertices."
    v = [[-x, y] for x, y, z in v_raw]
    w = texture.width
    h = texture.height
    vt = [[w * x, h * (1 - y)] for x, y in vt_raw]
    patches = []
    canvas_width = 0
    canvas_height = 0
    for i in range(int(len(vt) / 4)):
        patch = texture.crop(
            (
                custom_round(vt[i * 4 + 1][0]),
                custom_round(vt[i * 4 + 1][1]),
                custom_round(vt[i * 4 + 3][0]),
                custom_round(vt[i * 4 + 3][1]),
            )
        )
        canvas_width = max(canvas_width, v[i * 4][0] + patch.width)
        canvas_height = max(canvas_height, v[i * 4 + 2][1])
        patches.append(patch)
    canvas = Image.new(
        "RGBA",
        (
            custom_round(max(size["x"], canvas_width)),
            custom_round(max(size["y"], canvas_height)),
        ),
    )
    for i, patch in enumerate(patches):
        canvas.alpha_composite(
            patch.convert("RGBA").transpose(Image.Transpose.FLIP_TOP_BOTTOM),
            (
                custom_round(v[i * 4][0]),
                custom_round(v[i * 4 + 2][1] - patch.height),
            ),
        )
    # qiabayefu_2_n
    if canvas.width > size["x"] or canvas.height > size["y"]:
        bbox = canvas.getbbox()
        if bbox:
            left, upper, right, lower = bbox
            new_bbox = (0, 0, max(right, size["x"]), max(lower, size["y"]))
        else:
            new_bbox = (0, 0, size["x"], size["y"])
        canvas = canvas.crop(new_bbox)
    canvas = canvas.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    if saveMesh:
        rel_path = os.path.relpath(asset_group_path, input_root)
        out_dir = Path(output_root, rel_path)
        os.makedirs(out_dir / "mesh", exist_ok=True)
        canvas.save(out_dir / "mesh" / (layer["name"] + ".png"))
    return canvas


def get_primary(asset):
    # Returns typetree of the primary asset (as reported by the AssetBundle).
    bundle = asset.objects[1]  # m_PathID is always 1 for the AssetBundle
    if bundle.type.name != "AssetBundle":  # in case the above isn't true
        # print("Object at m_PathID=1 is not an AssetBundle.\nSearching for AssetBundle...")
        found = False
        for value in asset.values():
            if value.type.name == "AssetBundle":
                bundle = value
                # print("AssetBundle found at m_PathID=", bundle.path_id, ".", sep="")
                found = True
                break
        assert found, "No AssetBundle found."
    bundletree = bundle.read_typetree()
    # haitian_5
    primaryid = bundletree["m_Container"][-1][1]["asset"]["m_PathID"]
    primary = asset.objects[primaryid]
    return primaryid, primary.read_typetree()


def get_dependencies():
    # Returns dependency map linking asset files to their texture files.
    env = UnityPy.load(str(Path(input_root, "dependencies")))
    id, primary = get_primary(env.assets[0])
    dependencies = {}
    for m_Value in primary["m_Values"]:
        m_FileName = re.sub(r"^.*?(/painting/.*)?$", r"\g<1>", m_Value["m_FileName"])[
            1:
        ]
        # m_FileName = re.sub('^.*?(/painting(?:face)?/.*)?$', '\g<1>', m_Value['m_FileName'])[1:] # includes paintingface
        if m_FileName:
            # if m_FileName.endswith('_tex'):
            #     if m_Value['m_Dependencies']:
            #         print('Texture file includes dependencies:',  m_FileName)
            # elif not m_Value['m_Dependencies']:
            #     print('Non-texture file without dependencies:', m_FileName)
            dependencies.setdefault(m_FileName, m_Value["m_Dependencies"])
    return dependencies


def get_layers(asset, textures, layers={}, id=None, parent=None):
    if id is None:
        id, gameobject = get_primary(asset)
    else:
        gameobject = asset[id].read_typetree()

    if gameobject["m_Name"] == "shop_hx":
        return
    if gameobject["m_Name"] == "shadow":
        return
    if gameobject["m_Name"] == "Touch":
        return
    if gameobject["m_Name"] == "hx":
        return
    if "m_Component" not in gameobject:
        return

    children = None
    mesh_id = None
    entry = {}
    entry["name"] = gameobject["m_Name"]
    for ptr in gameobject["m_Component"]:
        component_id = ptr["component"]["m_PathID"]
        component = asset[component_id]
        tree = component.read_typetree()
        # print(gameobject["m_Name"],component.type.name,tree,"\n")
        if component.type.name == "RectTransform":
            entry["scale"] = tree["m_LocalScale"]
            if parent == None or entry["name"] == "layers":
                entry["scale"] = {"x": 1, "y": 1, "z": 1}
            entry["delta"] = tree["m_SizeDelta"]
            entry["pivot"] = tree["m_Pivot"]
            entry["rotation"] = tree["m_LocalRotation"]

            # calculate true m_LocalPosition
            anchormin = tree["m_AnchorMin"]
            anchormax = tree["m_AnchorMax"]
            anchorpos = tree["m_AnchoredPosition"]
            if parent is None:
                entry["bound"] = entry["delta"]
                entry["position"] = {
                    "x": entry["delta"]["x"] * entry["pivot"]["x"],
                    "y": entry["delta"]["y"] * entry["pivot"]["y"],
                }
            else:
                pl = layers[parent]
                entry["bound"] = {
                    "x": (
                        pl["bound"]["x"] * (anchormax["x"] - anchormin["x"])
                        + entry["delta"]["x"]
                    )
                    * entry["scale"]["x"],
                    "y": (
                        pl["bound"]["y"] * (anchormax["y"] - anchormin["y"])
                        + entry["delta"]["y"]
                    )
                    * entry["scale"]["y"],
                }  # bounding box width and height
                entry["position"] = {
                    "x": anchorpos["x"]
                    + pl["bound"]["x"]
                    * (anchormax["x"] - anchormin["x"])
                    * entry["pivot"]["x"]
                    + pl["bound"]["x"] * anchormin["x"]
                    - pl["bound"]["x"] * pl["pivot"]["x"],
                    "y": anchorpos["y"]
                    + pl["bound"]["y"]
                    * (anchormax["y"] - anchormin["y"])
                    * entry["pivot"]["y"]
                    + pl["bound"]["y"] * anchormin["y"]
                    - pl["bound"]["y"] * pl["pivot"]["y"],
                }  # pivot in relation to parent pivot
            if (gameobject["m_Name"] == "face" and "parent" not in layers[parent]) or (
                gameobject["m_Name"] == "face_sub" and layers[parent]["name"] == "face"
            ):
                entry["size"] = entry["delta"]
            children = tree["m_Children"]
        # bisimaiz
        if (
            component.type.name == "Transform"
            and children == None
            and "m_Children" in tree
        ):
            entry["scale"] = tree["m_LocalScale"]
            if parent == None or entry["name"] == "layers":
                entry["scale"] = {"x": 1, "y": 1, "z": 1}
            entry["delta"] = {"x": 0, "y": 0}
            entry["pivot"] = {"x": 0.5, "y": 0.5}
            entry["rotation"] = tree["m_LocalRotation"]
            entry["bound"] = {"x": 0, "y": 0}
            entry["position"] = {"x": 0, "y": 0}
            children = tree["m_Children"]
        if "mMesh" in tree:
            mesh_id = tree["mMesh"]["m_PathID"]
            sprite_id = tree["m_Sprite"]["m_PathID"]
            entry["size"] = tree["mRawSpriteSize"]
        # xiefeierde_3
        elif (
            "m_Sprite" in tree
            and entry["name"] != "face"
            and entry["name"] != "face_sub"
        ):
            entry["isImage"] = True
            mesh_id = 0
            sprite_id = tree["m_Sprite"]["m_PathID"]
            entry["size"] = entry["delta"]

    if mesh_id is not None:
        texas = {}
        for i in range(len(textures.assets)):
            texas = texas | textures.assets[i].objects
        try:
            entry["mesh"] = texas[mesh_id].read()
        except:
            # print("No mesh found.")
            pass
        try:
            sprite = texas[sprite_id].read_typetree()
            if "_shophx" not in sprite["m_Name"]:
                texture_id = sprite["m_RD"]["texture"]["m_PathID"]
                entry["texture"] = texas[texture_id].read()
        except:
            # do not report missing touming_tex
            if sprite_id not in [-1941817362335269276, -627025325541918145, 0]:
                print(entry["name"], "missing texture file")

    if parent is not None:
        entry["parent"] = parent

    layers[id] = entry

    if children is not None:
        for rt_ptr in children:
            rt_id = rt_ptr["m_PathID"]
            rt = asset[rt_id].read_typetree()
            child_id = rt["m_GameObject"]["m_PathID"]
            get_layers(asset, textures, layers, child_id, id)


def get_base_name(filename):
    """Strip variant suffixes exactly as in wrapped() to get the base name."""
    # Order alternatives from longest to shortest to handle overlaps like _bj1 vs _bj
    pattern = r"(_tex|_wjz|_bj1|_bj2|_bj|_hx|_ex|_rw|_n)+"
    return re.sub(pattern, "", filename).replace("_idolns", "_idol")


def some_heavy_lifting_tasks(painting_name):
    depmap = get_dependencies()
    depfiles = depmap.get("painting/{}".format(painting_name))

    # Collect local dependency files
    depfiles_ex_local = [
        "painting/{}".format(f.name)
        for f in Path(asset_group_path, "painting").iterdir()
        if (f.is_file() and get_base_name(painting_name) in f.name)
    ]
    # Collect asset warehouse dependency files
    depfiles_ex_warehouse = []
    if painting_warehouse_exist:
        depfiles_ex_warehouse = [
            "painting/{}".format(f.name)
            for f in painting_warehouse_dir.iterdir()
            if (f.is_file() and get_base_name(painting_name) in f.name)
        ]

    # Combine and deduplicate
    depfiles_ex = list(set(depfiles_ex_local + depfiles_ex_warehouse))
    # Combine and deduplicate dependency filenames
    all_dep_filenames = list(set(depfiles or []) | set(depfiles_ex))

    # Build list of actual existing file paths
    texture_paths = []
    for fn in all_dep_filenames:
        local_path = Path(asset_group_path, fn)
        if local_path.exists():
            texture_paths.append(str(local_path))
        else:
            source_path = Path(
                asset_warehouse_path, fn
            )  # fallback to original game assets
            if source_path.exists():
                texture_paths.append(str(source_path))

    # Load textures
    if texture_paths:
        textures = UnityPy.load(*texture_paths)
    else:
        textures = None

    local_p = Path(asset_group_path, "painting", painting_name)
    source_p = Path(asset_warehouse_path, "painting", painting_name)
    if local_p.exists():
        env = UnityPy.load(str(local_p))
    elif source_p.exists():
        env = UnityPy.load(str(source_p))

    layers = {}
    get_layers(env.assets[0], textures, layers)

    def get_position_box(layer, x=None, y=None, w=None, h=None):
        if x is None or y is None:
            x = layer["bound"]["x"] * layer["pivot"]["x"] - layer["position"]["x"]
            y = layer["bound"]["y"] * layer["pivot"]["y"] - layer["position"]["y"]
            w = layer["bound"]["x"]
            h = layer["bound"]["y"]
        if "parent" in layer:
            parent = layers[layer["parent"]]
            # xiaotiane_2:hx
            w *= parent["scale"]["x"]
            h *= parent["scale"]["y"]
            x = x * parent["scale"]["x"] - parent["position"]["x"]
            y = y * parent["scale"]["y"] - parent["position"]["y"]
            return get_position_box(parent, x, y, w, h)
        return [-x, -y, w - x, h - y]

    for i in layers:
        layer = layers[i]
        if "size" in layer:
            layer["box"] = get_position_box(layer)
    fix = [0, 0]
    rw_flag = False
    for i in layers:
        layer = layers[i]
        if "box" in layer:
            if "_rw" in layer["name"]:
                fix[0] = custom_round(layer["box"][0]) - layer["box"][0]
                fix[1] = custom_round(layer["box"][1]) - layer["box"][1]
                rw_flag = True
    # wuzang_n, wuzang_s, qiabayefu_2
    if rw_flag == False:
        for i in layers:
            layer = layers[i]
            if "box" in layer and "parent" not in layer:
                name = layer["name"]
                for i in layers:
                    layer = layers[i]
                    if (
                        "box" in layer
                        and "parent" in layer
                        and (layer["name"] == name or layer["name"] == "paint")
                    ):
                        fix[0] = custom_round(layer["box"][0]) - layer["box"][0]
                        fix[1] = custom_round(layer["box"][1]) - layer["box"][1]
                        break
                break
    for i in layers:
        layer = layers[i]
        if "box" in layer:
            if layer["name"] == "face":
                layer["box"][0] += fix[0] + face_fix.get(painting_name, [0, 0, 0, 0])[0]
                layer["box"][1] += fix[1] + face_fix.get(painting_name, [0, 0, 0, 0])[1]
                layer["box"][2] += fix[0] + face_fix.get(painting_name, [0, 0, 0, 0])[2]
                layer["box"][3] += fix[1] + face_fix.get(painting_name, [0, 0, 0, 0])[3]
            layer["box"][2] = (
                custom_round(layer["box"][0]) + layer["box"][2] - layer["box"][0]
            )
            layer["box"][3] = (
                custom_round(layer["box"][1]) + layer["box"][3] - layer["box"][1]
            )
            layer["box"][0] = custom_round(layer["box"][0])
            layer["box"][1] = custom_round(layer["box"][1])

    boxes = [layer["box"] for layer in layers.values() if "size" in layer]
    if boxes:
        x0, y0 = min(box[0] for box in boxes), min(box[1] for box in boxes)
        x1, y1 = max(box[2] for box in boxes), max(box[3] for box in boxes)
    for i in layers:
        layer = layers[i]
        if "box" in layer:
            layer["box"][0] = layer["box"][0] - x0
            layer["box"][1] = layer["box"][1] - y0
            layer["box"][2] = layer["box"][2] - x0
            layer["box"][3] = layer["box"][3] - y0
            if debug:
                print("box", layer["name"], layer["box"])
    try:
        master = Image.new("RGBA", (custom_round(x1 - x0), custom_round(y1 - y0)))
    except:
        print(painting_name, "failed")
        return

    if painting_name == "changfeng_2":
        front_layer = None
        for key, value in layers.items():
            if value.get("name") == "changfeng_2_bj":
                front_layer = key
                break
        if front_layer:
            layers[front_layer] = layers.pop(front_layer)

    canvases = []
    for i in layers:
        layer = layers[i]
        if "mesh" in layer and "texture" in layer:
            canvas = get_canvas(layer)
            canvas = canvas.resize(
                (
                    custom_round(
                        canvas.width
                        * ((layer["box"][2] - layer["box"][0]) or layer["size"]["x"])
                        / layer["size"]["x"]
                    ),
                    custom_round(
                        canvas.height
                        * ((layer["box"][3] - layer["box"][1]) or layer["size"]["y"])
                        / layer["size"]["y"]
                    ),
                ),
                Image.BILINEAR,
            ).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            canvases.append([canvas, layer])
        elif "texture" in layer:
            canvas = layer["texture"].image.convert("RGBA")
            if saveMesh:
                os.makedirs(out_dir / "mesh", exist_ok=True)
                canvas.save(out_dir / "mesh" / (layer["name"] + ".png"))
            canvas = canvas.resize(
                (
                    custom_round((layer["box"][2] - layer["box"][0]) or canvas.width),
                    custom_round((layer["box"][3] - layer["box"][1]) or canvas.height),
                ),
                Image.BILINEAR,
            ).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            canvases.append([canvas, layer])
        elif layer["name"] == "face":
            canvas = "face"
            canvases.append([canvas, layer])
        elif layer["name"] == "face_sub":
            canvas = "face_sub"
            canvases.append([canvas, layer])
    return master, canvases


def wrapped(painting_name, id_dict={}, debug=False, compress=False, use_webp=False):
    if "_tex" in painting_name:
        print('Please enter the filename without the "_tex" suffix.')
        return
    if painting_name in [
        "mat",
        "mat_v1f1",
        "jinluhao_hx",
        "jinluhao_n_hx",
        "dafeng_6_shophx",
        "haifeng_3_n_rw",
    ]:
        return

    # --- Setup Dynamic Output Directory ---
    # input: AssetBundles\x\y\z\(painting & paintingface)
    # output: output\x\y\z\(images)
    rel_path = os.path.relpath(asset_group_path, input_root)
    out_dir = Path("output", rel_path)
    ext = ".webp" if use_webp else ".png"

    # Use to check if output file already exist
    ext = ".webp" if use_webp else ".png"

    base_name = get_base_name(painting_name)
    filename = painting_name
    if id_dict:
        filename = id_dict.get(base_name, "999999") + "_" + painting_name

    print("\nStart", painting_name)
    os.makedirs(out_dir, exist_ok=True)

    face0_flag = False
    heavy_lifting_tasks_done = False

    # A list of suffixes to try, including empty string
    suffixes = ["", "_hx", "_wjz"]
    base_dirs = [Path(asset_group_path, "paintingface")]
    if paintingface_warehouse_exist:
        base_dirs.append(paintingface_warehouse_dir)

    faces = None
    for base_dir in base_dirs:
        for suffix in suffixes:
            candidate = f"{get_base_name(painting_name)}{suffix}"
            face_file = Path(base_dir, candidate)
            if face_file.exists():
                faces = UnityPy.load(str(face_file))
                if len(faces.assets) != 0:
                    break
        if faces is not None and len(faces.assets) != 0:
            break

    if faces is not None and len(faces.assets) != 0:
        face_sub = {}
        for value in faces.assets[0].values():
            if value.type.name == "Texture2D":
                sub = value.read()
                if "_sub" in sub.m_Name:
                    face_sub[sub.m_Name] = sub
        for value in faces.assets[0].values():
            if value.type.name == "Texture2D":
                face = value.read()
                if face.m_Name == "0":
                    face0_flag = True

                # Skip if this face is already processed
                face_path = out_dir / f"{filename}.{face.m_Name}{ext}"
                if face_path.is_file() and face_path.stat().st_size > 0:
                    print(
                        f"Skipping {filename}.{face.m_Name}, already exists in {out_dir}"
                    )
                    continue

                if ("_sub" in face.m_Name) or (debug and face.m_Name != "1"):
                    continue

                # Only do these tasks (once) if the file didn't got skip
                if not heavy_lifting_tasks_done:
                    master, canvases = some_heavy_lifting_tasks(painting_name)
                    heavy_lifting_tasks_done = True
                    if master is None:
                        return

                copy = master.copy()
                for canvaslayer in canvases:
                    layer = canvaslayer[1]
                    canvas = canvaslayer[0]
                    if canvas == "face":
                        canvas = face.image.convert("RGBA")
                        # bolisi
                        canvas = canvas.resize(
                            (
                                custom_round(
                                    (layer["box"][2] - layer["box"][0]) or canvas.width
                                ),
                                custom_round(
                                    (layer["box"][3] - layer["box"][1]) or canvas.height
                                ),
                            ),
                            Image.BILINEAR,
                        ).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                    # xiaoyue_2
                    elif canvas == "face_sub":
                        if face_sub.get(face.m_Name + "_sub"):
                            canvas = face_sub.get(face.m_Name + "_sub").image.convert(
                                "RGBA"
                            )
                            canvas = canvas.resize(
                                (
                                    custom_round(
                                        (layer["box"][2] - layer["box"][0])
                                        or canvas.width
                                    ),
                                    custom_round(
                                        (layer["box"][3] - layer["box"][1])
                                        or canvas.height
                                    ),
                                ),
                                Image.BILINEAR,
                            ).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                        else:
                            continue
                    # changdao_g:hx
                    if layer["rotation"]["z"] != 0:
                        angle_rad = 2 * math.atan2(
                            layer["rotation"]["z"], layer["rotation"]["w"]
                        )
                        w, h = canvas.size
                        canvas = canvas.rotate(
                            -math.degrees(angle_rad),
                            expand=True,
                            resample=Image.BILINEAR,
                        )
                        new_w, new_h = canvas.size
                        px, py = layer["pivot"]["x"] * w, layer["pivot"]["y"] * h
                        dx, dy = px - w / 2, py - h / 2
                        layer["box"][0] += px - (
                            new_w / 2
                            + dx * math.cos(angle_rad)
                            - dy * math.sin(angle_rad)
                        )
                        layer["box"][1] += py - (
                            new_h / 2
                            + dx * math.sin(angle_rad)
                            + dy * math.cos(angle_rad)
                        )
                    # qiye_4
                    if copy.width < canvas.width + custom_round(
                        layer["box"][0]
                    ) or copy.height < canvas.height + custom_round(layer["box"][1]):
                        new_copy = Image.new(
                            "RGBA",
                            (
                                max(
                                    copy.width,
                                    canvas.width + custom_round(layer["box"][0]),
                                ),
                                max(
                                    copy.height,
                                    canvas.height + custom_round(layer["box"][1]),
                                ),
                            ),
                        )
                        new_copy.alpha_composite(copy, (0, 0))
                        copy = new_copy
                    copy.alpha_composite(
                        canvas,
                        (custom_round(layer["box"][0]), custom_round(layer["box"][1])),
                    )

                copy = copy.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

                # --- SAVE COMPRESSED/ORIGINAL ---
                save_image(copy, str(face_path), compress, use_webp)
    else:
        print(painting_name, " - no face found")
        face0_flag = True

    if face0_flag:
        output_filename = f"{filename}"
    else:
        output_filename = f"{filename}.0"
    master_path = out_dir / f"{output_filename}{ext}"
    if master_path.is_file() and master_path.stat().st_size > 0:
        print(f"Skipping {output_filename}, already exists in {out_dir}")
        return

    # Only do these tasks (once) if the file didn't got skip
    if not heavy_lifting_tasks_done:
        master, canvases = some_heavy_lifting_tasks(painting_name)
        heavy_lifting_tasks_done = True
        if master is None:
            return

    for canvaslayer in canvases:
        layer = canvaslayer[1]
        canvas = canvaslayer[0]
        if canvas == "face" or canvas == "face_sub":
            continue
        if layer["rotation"]["z"] != 0:
            angle_rad = 2 * math.atan2(layer["rotation"]["z"], layer["rotation"]["w"])
            w, h = canvas.size
            canvas = canvas.rotate(
                -math.degrees(angle_rad), expand=True, resample=Image.BILINEAR
            )
            new_w, new_h = canvas.size
            px, py = layer["pivot"]["x"] * w, layer["pivot"]["y"] * h
            dx, dy = px - w / 2, py - h / 2
            layer["box"][0] += px - (
                new_w / 2 + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
            )
            layer["box"][1] += py - (
                new_h / 2 + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
            )
        if master.width < canvas.width + custom_round(
            layer["box"][0]
        ) or master.height < canvas.height + custom_round(layer["box"][1]):
            new_master = Image.new(
                "RGBA",
                (
                    max(master.width, canvas.width + custom_round(layer["box"][0])),
                    max(master.height, canvas.height + custom_round(layer["box"][1])),
                ),
            )
            new_master.alpha_composite(master, (0, 0))
            master = new_master
        master.alpha_composite(
            canvas, (custom_round(layer["box"][0]), custom_round(layer["box"][1]))
        )

    master = master.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    # --- SAVE COMPRESSED/ORIGINAL ---
    save_image(master, str(master_path), compress, use_webp)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "file", nargs="?", help="the name of the painting assetbundle file"
    )
    # Added compress and webp flag
    parser.add_argument(
        "-c", "--compress", action="store_true", help="Compress PNG via quantization"
    )
    parser.add_argument(
        "-w", "--webp", action="store_true", help="Output as WebP instead of PNG"
    )
    args = parser.parse_args()

    id_dict = get_id_dict()

    debug = False
    mp = False

    # Check if the original game file folder exist
    painting_warehouse_dir = Path(asset_warehouse_path, "painting")
    painting_warehouse_exist = asset_warehouse_path and painting_warehouse_dir.exists()
    paintingface_warehouse_dir = Path(asset_warehouse_path, "paintingface")
    paintingface_warehouse_exist = (
        asset_warehouse_path and paintingface_warehouse_dir.exists()
    )
    if args.file:
        # Single file mode: ensure asset_group_path is set correctly
        asset_group_path = input_root
        # Define the potential paths for the requested file
        local_path = Path(asset_group_path, "painting", args.file)
        warehouse_path = (
            Path(painting_warehouse_dir, args.file)
            if painting_warehouse_exist
            else None
        )

        # Check if the file exists in either the local folder or the warehouse
        if local_path.is_file() or (warehouse_path and warehouse_path.is_file()):
            wrapped(args.file, id_dict, debug, args.compress, args.webp)
        else:
            print(
                f"\nError: '{args.file}' was not found in '{local_path.parent}' or the warehouse directory. Stopping.\n"
            )
    else:
        # Batch mode: find all base directories that contain a "painting" subfolder
        base_dirs = set()
        for dirpath, dirnames, _ in os.walk("AssetBundles"):
            if "painting" in dirnames:
                base_dirs.add(dirpath)

        for base in base_dirs:
            print(f"\n--- Processing base: {base} ---")
            # Set the global asset_group_path to this base directory
            asset_group_path = base

            # Gather all painting asset files (non-_tex) in this base's painting folder
            paintingfiles = []
            basenames = set()

            # First pass: Get standard files and basenames from _tex files
            for root2, dirs, files in os.walk(Path(asset_group_path, "painting")):
                for file in files:
                    if not file.endswith("_tex"):
                        paintingfiles.append(file)
                    if painting_warehouse_exist:
                        # Extract base name (junzhu_5_n_rw_tex -> junzhu_5)
                        # to find related assets in warehouse folder
                        base_name = get_base_name(file)
                        basenames.add(base_name)

            # Second pass: add missing source painting files that match the same base name
            if painting_warehouse_exist and basenames:
                for source_file in painting_warehouse_dir.iterdir():
                    if source_file.is_file() and not source_file.name.endswith("_tex"):
                        base_name = get_base_name(source_file.name)
                        if (
                            base_name in basenames
                            and source_file.name not in paintingfiles
                        ):
                            paintingfiles.append(source_file.name)
            if mp:
                import multiprocessing
                from functools import partial

                multiprocessing.Pool().map(
                    partial(
                        wrapped,
                        id_dict=id_dict,
                        debug=debug,
                        compress=args.compress,
                        use_webp=args.webp,
                    ),
                    paintingfiles,
                )
            else:
                for file in paintingfiles:
                    wrapped(file, id_dict, debug, args.compress, args.webp)
