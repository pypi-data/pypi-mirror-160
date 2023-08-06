""""

"""

def extension_metadata():
  import importlib.resources  # pylint: disable=import-error,no-name-in-module
  return {
      "primary_extension": True,
      "priority": 100,
      "setups": {
          "CAS_Production": "dips://dirac.ihep.ac.cn:9135/Configuration/Server",
          "CAS_Production-cert": "dips://dirac.ihep.ac.cn:9135/Configuration/Server",
      },
      "default_setup": "CAS_Production",
      "web_resources": {
          "static": [importlib.resources.files("IHEPDIRAC") / "WebApp" / "static"],  # pylint: disable=no-member
      },
  }
