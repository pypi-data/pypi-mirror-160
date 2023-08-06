import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-nat-asg-provider",
    "version": "0.0.2",
    "description": "An AWS CDK library providing NAT instances that are each placed in their own auto scaling group to improve fault tolerance and availability.",
    "license": "Apache-2.0",
    "url": "https://github.com/fonzcastellanos/cdk-nat-asg-provider.git",
    "long_description_content_type": "text/markdown",
    "author": "Alfonso Castellanos<dev@alfonsocastellanos.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/fonzcastellanos/cdk-nat-asg-provider.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_nat_asg_provider",
        "cdk_nat_asg_provider._jsii"
    ],
    "package_data": {
        "cdk_nat_asg_provider._jsii": [
            "cdk-nat-asg-provider@0.0.2.jsii.tgz"
        ],
        "cdk_nat_asg_provider": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.26.0, <3.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
