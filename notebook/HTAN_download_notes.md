# HTAN Data Download Notes

## Downloading Multiple Files from HTAN Portal

### Step 1 — Get the Manifest
1. Go to [humantumoratlas.org](https://humantumoratlas.org) and filter for your files of interest
2. Select the files and click **"Generate DRS manifest"** → download as CSV (`crdc_gc_manifest.csv`)

### Step 2 — Convert Manifest to JSON
gen3-client requires a JSON manifest, not CSV. Run this Python script to convert:

```python
import pandas as pd
import json

df = pd.read_csv(r"path\to\crdc_gc_manifest.csv")
df['object_id'] = df['drs_uri'].str.split('/').str[-1]
manifest = [{'object_id': oid} for oid in df['object_id']]

with open(r"path\to\gen3_manifest.json", 'w') as f:
    json.dump(manifest, f)

print("Done:", len(manifest), "files")
```

### Step 3 — Set Up gen3-client (first time only)
1. Download gen3-client from [https://github.com/uc-cdis/cdis-data-client/releases/latest](https://github.com/uc-cdis/cdis-data-client/releases/latest)
2. Unzip and add to PATH (e.g. `C:\Program Files\gen3-client\`)
3. Log in to [nci-crdc.datacommons.io](https://nci-crdc.datacommons.io) via RAS → Login.gov (use personal email)
4. Go to Profile → Create API key → download `credentials.json`
5. Configure your profile:

```
gen3-client configure --profile=htan --cred="path\to\credentials.json" --apiendpoint=https://nci-crdc.datacommons.io
```

### Step 4 — Download Files
> **Important:** gen3-client must be run in **cmd**, not PowerShell. Open cmd by typing `cmd` in your terminal first.

```
cmd
gen3-client auth --profile=htan
gen3-client download-multiple --profile=htan --manifest="path\to\gen3_manifest.json" --download-path="path\to\save\folder" --numparallel 4 --skip-completed
```

- `--numparallel 4` speeds up download by running 4 files in parallel (safe for ~700MB files)
- `--skip-completed` skips already downloaded files if you need to resume

---

## Notes
- All open access files are **free to download** — no cost
- Images are **OME-TIFF** format — channel metadata is embedded in the file header (no separate CSV needed)
- Level 2 = raw multichannel images; Level 3 = per-cell quantification tables (CSV)
- To read channel names from an OME-TIFF:

```python
import tifffile
import xml.etree.ElementTree as ET

with tifffile.TiffFile(r"path\to\file.ome.tif") as tif:
    root = ET.fromstring(tif.ome_metadata)
    for element in root.iter():
        if element.tag == "{http://www.openmicroscopy.org/Schemas/OME/2016-06}Channel":
            print(element.attrib['Name'])
```
