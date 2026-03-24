# Azur Lane Painting Reconstruction

This script is a fork of [Senkin219's script](https://github.com/Senkin219/AzurLanePainting) with more flexible input directory, add fallback to get related asset files from base game AssetBundles folder if they are absent from the input folders. And some minor change.

## Usage
   - From this:

<img width="336" height="137" alt="image" src="https://github.com/user-attachments/assets/93989451-a7a6-4569-a8ef-defc080c54cb" />

   - To this:      (this girl has 9 different expressions)

<img width="1654" height="833" alt="image" src="https://github.com/user-attachments/assets/73c762ae-6b50-4063-9df6-5ff741c7e698" />


### Setup

Arrange your files in the following structure:

```
Working Directory/
├── main.py
├── AssetBundles/
│   ├── dependencies              # Get this file from game folder
│   ├── painting/
│   │   ├── changfeng_2           # Example painting asset
│   │   ├── changfeng_2_tex       # Corresponding texture asset
│   │   ├── changfeng_2_rw_tex    # Corresponding texture asset
│   │   └── changfeng_2_bj_tex    # Corresponding texture asset
│   ├── paintingface/
│   │   └── changfeng_2           # Face asset for the painting
│   ├── ship A/skin B/.../
│       └── painting/             # Works with any sub "painting" folder       
│           └── adiliao_3_tex     # Can works even when related files are missing 
│                                 # (require AssetBundles path in main.py)
│
├── ship_skin_template.json       # Optional, for structured output
├── ship_data_group.json          # Optional, for structured output
└── secretary_special_ship.json   # Optional, for structured output

(optional)
...
└── AssetBundles/                 # Game data folder
    ├── painting/
    │   ├── adiliao_3             # 
    │   ├── adiliao_3_n           # Auto process related files
    │   ├── adiliao_3_rw_tex      # to build reconstruct paintings
    │   └── adiliao_3_rw_n_tex    # 
    └── paintingface/
        └── adiliao_3             # 
```

   - Place `main.py` in the root of your working directory.
   - Store painting assets under `AssetBundles/painting`.
   - Store face assets under `AssetBundles/paintingface`.
   - Ensure the `dependencies` file is included in the `AssetBundles` directory.

### Running the Script

- **To process all available files:**
  
  ```bash
  python main.py
  ```
  
- **To process a specific file:**
  
  ```bash
  python main.py changfeng_2
  ```

- **Add -m to process all files with multithread:**
  
  ```bash
  python main.py -m
  ```

- **Add -c to lower PNG size:**
  
  ```bash
  python main.py -c
  ```

- **Add -w to export as WEBP for further reduce the output size:**
  
  ```bash
  python main.py -w
  ```
  
### Output

- Reconstructed paintings are saved in the `output2` folder.
- To generate numbered filenames, add `ship_skin_template.json`, `ship_data_group.json`, and `secretary_special_ship.json` to your working directory. These files can be found [here](https://github.com/AzurLaneTools/AzurLaneData/tree/main/CN/ShareCfg).

## Known Issues

- Some assets contain both censored and uncensored versions of paintings (e.g., `npcshengluyisi_5_n`); the script only processes the first version encountered.

