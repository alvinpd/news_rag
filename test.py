import chromadb
from rich import print
from langchain.docstore.document import Document
from langchain.text_splitter import MarkdownTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores.chroma import Chroma
from langchain_community import embeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

local_llm = ChatOllama(model="mistral")

# RAG
def rag(retriever, question):
        prompt_template = """Answer the question based only on the following context:
        {context}
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)

        chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | local_llm
                | StrOutputParser()
        )
        result = chain.invoke(question)
        print(result)

# Start Chroma: chroma run --path /dbpath

client = chromadb.HttpClient(host="localhost", port=8000)
vectorstore = Chroma(
        collection_name="news",
        client=client,
        embedding_function= embeddings.OllamaEmbeddings(model="nomic-embed-text"))

splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=20)
markdown_text = """
# Key events in developed markets next week

URL: key-events-in-developed-markets-next-week-202403081258
Time: 2024-03-08 12:58:33

Next week sees a flurry of�US�data releases, including CPI, retail sales, and industrial production - although we�don't�expect these to have any major�impact on the Fed's decision-making. Over in the eurozone, surveys are likely to hint at weakness in�industrial production data. In the UK, the Bank of England will be keeping a close eye on wage growth.

## US: We see a 0.3% MoM increase in February CPI

Federal Reserve Chair Jerome Powell�s testimony to Congress was perhaps not quite as hawkish as feared in the wake of strong jobs, growth and inflation data. He suggested that officials are �not far� from having the confidence to �dial back� on the restrictiveness of monetary policy. This week�s data calendar includes CPI, retail sales and industrial production, but on balance, they are unlikely to be weak enough to trigger the Fed choosing to ease policy imminently. Core inflation was far too hot for comfort last month, rising 0.4% month-on-month rather than the 0.2% or below that we'd want to see to before gaining any confidence that inflation is returning to 2% year-on-year. With housing dynamics looking more unsettled and recent insurance and medical cost hikes still coming through, we look for a 0.3% MoM increase, which remains too high for the Fed.

Meanwhile, retail sales should rebound after January�s weather-related weakness. We already know car sales were firm in February, while higher gasoline prices should also be supportive. However, the control group � which is more closely aligned with broader consumer spending trends by stripping out some of the more volatile items � is unlikely to remain strong. Industrial production may post another MoM decline given the ISM manufacturing index has contracted for 16 consecutive months. All in all, the Fed is increasingly inclined to move policy back to a more neutral level, but next week�s data won�t be enough to trigger a near-term move. We continue to favour June as the starting point for rate cuts.

## Eurozone: Surveys hint at weak industrial production data

It�s a light week for eurozone data, but industrial production will be interesting to look out for. December saw a large jump in production, which wiped out a full year of declines. This was mainly due to Irish production figures, though, which are notorious for their volatility thanks to contract manufacturing and outsourcing. Other countries also saw a small uptick on average. It will be interesting to see whether this jump was a one-off or whether there is more of a structural element to it. Surveys suggest the former, although manufacturers remain downbeat on production and orders for the moment. If January does turn out strong, this would be an upside for first-quarter GDP growth.

## Wage growth the highlight for the Bank of England next week

The Bank of England will be closely monitoring next week�s wage growth figures, in particular those covering the private sector, as it continues to mull over the timing of its first rate cut. Alongside services inflation, this is a critical input into that decision and while progress in the official data has been improving, it�s a slow-moving picture. The Bank of England can take some comfort in the fact that wage growth expectations in its survey of CFOs have finally dipped below 5%, but it will still want to see further progress � particularly in light of a sizeable increase in the National Living Wage in April.

Given that April and May are also key months for annual index-linked price rises in the service sector, we think the BoE will want to see CPI data for both of those months before cutting rates. That pitches June as the first realistic data for a cut, though August remains more likely in our opinion. We�ll also get monthly GDP figures for January, and these have been pretty volatile recently. Expect a rebound, linked in part to better retail figures at the start of the year. First-quarter GDP is likely to be positive when we get the numbers in a couple of months, marking the end of a very shallow technical recession for the UK.

Key events in developed markets next week

Source: Refinitiv, ING

Read the original analysis:�Key events in developed markets next week

"""

#documents = splitter.create_documents([markdown_text])
#vectorstore.add_documents(documents=documents)

rag(vectorstore.as_retriever(),
    "What is the outlook for gold?"
    )
