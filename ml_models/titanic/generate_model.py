from ml_models.processing import load_dataset, save_pipeline
from ml_models.titanic.pipeline import pipeline


def run_training() -> None:
    df = load_dataset(file_name="titanic/train.csv")
    X = df[["Pclass", "Sex", "Age", "Fare"]]
    y = df["Survived"]

    pipeline.fit(X, y)
    save_pipeline(pipeline=pipeline, file_name="titanic_predict_model.pkl")


if __name__ == "__main__":
    run_training()
