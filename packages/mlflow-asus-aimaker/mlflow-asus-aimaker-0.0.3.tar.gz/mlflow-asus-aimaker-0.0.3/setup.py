from setuptools import setup, find_packages

setup(
    name="mlflow-asus-aimaker",
    version="0.0.3",
    description="MLflow plugin for ASUS AI-Maker",
    packages=find_packages(),
    install_requires=["mlflow", "AIMaker"],
    entry_points={
        "mlflow.tracking_store": "file-plugin=mlflow_plugin.plugin_rest_store:PluginRestStore",
        "mlflow.model_registry_store": "file-plugin=mlflow_plugin.plugin_model_rest_store:PluginRegistryRestStore"
    },
)
