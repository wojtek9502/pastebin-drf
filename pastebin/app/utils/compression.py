import zstd


class NoteCompressionService:
    @staticmethod
    def compress(text: str) -> bytes:
        return zstd.compress(text.encode('utf-8'), 1)

    @staticmethod
    def decompress(compressed: bytes) -> str:
        return zstd.decompress(compressed).decode('utf-8')