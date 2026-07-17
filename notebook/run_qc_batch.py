"""
Batch QC for tissue fold/lost detection across all .ome.tif files in main_dir,
parallelized across CPU cores.

Usage:
    python run_qc_batch.py
"""
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd
import qc_tissue_fold_lost as qc


def qc_single_image(main_dir, file_name, qc_folder):
    round_dna_list = []
    qc_csv = pd.DataFrame()
    flagged_bounds = []
    print(f'Processing {file_name} ...')
    image_test = qc.QC_Fold_Lost(main_dir=main_dir, filename=file_name)
    for channel in list(image_test.full_image.biomarker_channel):
        if 'dna(' in channel:
            round_dna_list.append(channel)
    
    
    save_path = os.path.join(qc_folder, file_name.split(".")[0])
    for round_dna in round_dna_list:
        image_test.tile_disagreement(round_dna=round_dna, tile=32, min_foreground=0.05)
        image_test.flag_folds(k=8)
        image_test.plot_flagged_tiles(save_path=save_path, show=False)
        flagged_bounds.extend(image_test.get_flagged_tile_bounds())
        qc_csv = pd.concat([qc_csv, pd.DataFrame([image_test.get_qc_record()])], ignore_index=True)
        qc_csv.to_csv(os.path.join(save_path, f'{file_name.split(".")[0]}_qc.csv'), index=False)

    bounds_df = pd.DataFrame(flagged_bounds)
    bounds_df.to_csv(os.path.join(save_path, f'{file_name.split(".")[0]}_flagged_bounds.csv'), index=False)

    return file_name


if __name__ == "__main__":
    root_dir = r'D:\thu\HTAN\images'

    # each entry: (main_dir, qc_folder). Processed one at a time, in order --
    # the ProcessPoolExecutor `with` block below blocks until every file in
    # a dataset finishes before moving on to the next entry.
    datasets = [
        (os.path.join(root_dir, 'ILC', 'level_2'), os.path.join(root_dir, 'QC_Fold_Lost', 'ILC')),
        # add more (main_dir, qc_folder) tuples here to chain more datasets unattended
    ]

    max_workers = max(1, os.cpu_count() - 1)

    for main_dir, qc_folder in datasets:
        files = [f for f in os.listdir(main_dir) if f.endswith('.ome.tif')]
        print(f"[{main_dir}] Processing {len(files)} files with {max_workers} workers")

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(qc_single_image, main_dir, f, qc_folder): f
                for f in files
            }
            for future in as_completed(futures):
                f = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"{f} failed: {e}")

        print(f"[{main_dir}] Done.")

    print("All datasets done.")
