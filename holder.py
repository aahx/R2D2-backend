        # # Loading prospect information
        # loader = TextLoader(prospect_info)
        # data = loader.load()
        # print(f"You have {len(data)} main document(s)")

        # # Split documents to avoid token limits and enable prompt engineering; Will be taking chunks and map_reducing
        # text_splitter = RecursiveCharacterTextSplitter(
        #     chunk_size = 1000,
        #     chunk_overlap  = 0
        # )
        # docs = text_splitter.split_documents(data)
        # print (f"You now have {len(docs)} split documents")
