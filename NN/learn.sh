# creates bottlenecks in folder "bottlenecks2", learns NN based on classes in folder "dataset"

#rm -rf bottleneck2
rm -rf summaries/*
python retrain.py --image_dir=dataset/ --bottleneck_dir=bottleneck2/ --how_many_training_steps=500 --output_graph=trained_model/retrained_graph.pb --output_labels=trained_model/retrained_labels.txt --summaries_dir=summaries