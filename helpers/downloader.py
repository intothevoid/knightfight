import os
import urllib.request
import zipfile

STOCK_FISH_WIN_URL = "https://stockfishchess.org/files/stockfish_15.1_win_x64_avx2.zip"
STOCK_FISH_LINUX_URL = (
    "https://stockfishchess.org/files/stockfish_15.1_linux_x64_avx2.zip"
)


def download_stockfish(stockfish_path: str) -> None:
    """
    Download stockfish engine if not found
    """
    # MACOS and Linux
    if not os.name == "nt":
        if not os.path.exists(stockfish_path):
            # Download stockfish from URL
            url = STOCK_FISH_LINUX_URL
            urllib.request.urlretrieve(url, "stockfish.zip")

            # Extract stockfish
            with zipfile.ZipFile("stockfish.zip", "r") as zip_ref:
                zip_ref.extractall("assets/engines/")

            # Remove the downloaded zip file
            os.remove("stockfish.zip")
    else:
        # Windows
        if not os.path.exists("assets/engines/stockfish.exe"):
            # If not, prompt user for download
            response = input(
                "Stockfish engine not found. Would you like to download it now? (yes/no)"
            )
            if response.lower() == "yes":
                # Download stockfish from URL
                url = STOCK_FISH_WIN_URL
                urllib.request.urlretrieve(url, "stockfish.zip")

                # Extract stockfish
                with zipfile.ZipFile("stockfish.zip", "r") as zip_ref:
                    zip_ref.extractall("assets/engines/")

                # Remove the downloaded zip file
                os.remove("stockfish.zip")

                # Rename the extracted file
                os.rename(
                    "assets/engines/stockfish_15.1_win_x64_avx2.exe",
                    "assets/engines/stockfish.exe",
                )


# use wget to download stockfish
def download_stockfish_wget(stockfish_path: str) -> None:
    """
    Download stockfish engine if not found
    """
    if not os.path.exists(stockfish_path):
        # Download stockfish from URL
        if os.name == "nt":
            url = STOCK_FISH_WIN_URL
            os.system(f"wget {url} -O stockfish.zip")

            # Extract stockfish
            with zipfile.ZipFile("stockfish.zip", "r") as zip_ref:
                zip_ref.extractall("assets/engines/")

            # Remove the downloaded zip file
            os.remove("stockfish.zip")

            # Rename the extracted file
            os.rename(
                "assets/engines/stockfish_15.1_win_x64_avx2.exe",
                "assets/engines/stockfish.exe",
            )
        else:
            url = STOCK_FISH_LINUX_URL
            os.system(f"wget {url} -O stockfish.zip")

            # Extract stockfish
            with zipfile.ZipFile("stockfish.zip", "r") as zip_ref:
                zip_ref.extractall("assets/engines/")

            # Remove the downloaded zip file
            os.remove("stockfish.zip")

            # rename the extracted file
            os.rename(
                "assets/engines/**/stockfish_15.1_linux_x64_avx2",
                "assets/engines/stockfish",
            )
