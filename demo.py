from src.pipeline.train_pipeline import TrainPipeline

pipe = TrainPipeline()
pipe.start_data_ingestion()
pipe.start_data_validation()
pipe.start_data_transformation()