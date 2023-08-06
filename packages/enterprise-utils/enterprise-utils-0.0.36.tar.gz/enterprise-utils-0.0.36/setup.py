import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "enterprise-utils",
    "version": "0.0.36",
    "description": "@professionalaf/enterprise-utils",
    "license": "Apache-2.0",
    "url": "https://github.com/professionalaf/enterprise-utils.git",
    "long_description_content_type": "text/markdown",
    "author": "maafk<maafk@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/professionalaf/enterprise-utils.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "enterprise_utils",
        "enterprise_utils._jsii"
    ],
    "package_data": {
        "enterprise_utils._jsii": [
            "enterprise-utils@0.0.36.jsii.tgz"
        ],
        "enterprise_utils": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.25.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.62.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
