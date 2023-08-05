import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "renovosolutions.aws-cdk-aws-ipam",
    "version": "0.0.107",
    "description": "AWS CDK Construct Library to help create redirects on AWS application load balancers",
    "license": "Apache-2.0",
    "url": "https://github.com/RenovoSolutions/cdk-library-elbv2-redirect.git",
    "long_description_content_type": "text/markdown",
    "author": "Renovo Solutions<webmaster+cdk@renovo1.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/RenovoSolutions/cdk-library-elbv2-redirect.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "ipam",
        "ipam._jsii"
    ],
    "package_data": {
        "ipam._jsii": [
            "cdk-library-elbv2-redirect@0.0.107.jsii.tgz"
        ],
        "ipam": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.33.0, <3.0.0",
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
