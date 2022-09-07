from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import LogisticRegression

preprocessor = ColumnTransformer(
    transformers=[
        ("Fare", SimpleImputer(strategy="mean"), ["Fare"]),
        ("Age", SimpleImputer(strategy="mean"), ["Age"]),
        ("Sex", OrdinalEncoder(), ["Sex"]),
    ],
    remainder="passthrough",
)
model = LogisticRegression(penalty="l2", max_iter=10000, solver="sag", random_state=0)
pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
