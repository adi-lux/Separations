from gensim.models import KeyedVectors  # KeyedVectors

    """Generates the database that will be used for the Separator game.
    It will take several minutes to create.
    """

    mod = KeyedVectors.load_word2vec_format(
                "information/GoogleNews-vectors-negative300.bin.gz", binary=True )

    mod.save("information/words.bin")