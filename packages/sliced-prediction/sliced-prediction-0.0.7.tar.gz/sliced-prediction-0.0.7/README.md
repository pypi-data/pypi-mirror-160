# sliced-prediction
## Installation & Use

```shell
# Install sliced-prediction
> pip install sliced-prediction

> sliced-prediction --help
```

## Example
```shell
sliced-prediction \
--overlap_width_ratio 0 \
--overlap_height_ratio 0 \
--slice_width 1024 \
--slice_height 1024 \
--input_directory ./tests/data \
--output_manifest_file ./tmp/manifest.jsonl \
--model_path ./tmp/best.pt \
--confidence_threshold .2 \
--device cpu
```