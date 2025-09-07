from setuptools import setup, find_packages

setup(
    name="billing-dashboard",
    version="1.0.0",
    description="Interactive billing operations dashboard",
    author="Francisco Sabena",
    author_email="alfredo.sabena@mi.unc.edu.ar",
    packages=find_packages(),
    install_requires=[
        "dash>=2.18.0",
        "dash-bootstrap-components>=1.6.0",
        "plotly>=5.22.0",
        "pandas>=2.2.0",
        "numpy>=1.26.0",
        "scikit-learn>=1.4.0",
        "seaborn>=0.13.0",
        "matplotlib>=3.9.0",
        "folium>=0.16.0",
        "dash-extensions>=1.0.4",
        "gunicorn>=23.0.0",
    ],
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
)
