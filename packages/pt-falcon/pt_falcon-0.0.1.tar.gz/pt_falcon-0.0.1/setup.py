from distutils.core import setup


def setup_package():
    setup(
        name="pt_falcon",
        version='0.0.1',
        author="Koen Vossen",
        author_email="info@koenvossen.nl",
        url="",
        packages=[],
        license="GPL-3.0",
        description="pt_falcon is a performance optimized container for performance and tracking data.",
        long_description="pt_falcon is a performance optimized container for performance and tracking data.",
        long_description_content_type="text/markdown",
        classifiers=[],
        install_requires=[],
    )


if __name__ == "__main__":
    setup_package()
