import requests

response = requests.post('https://pdfswitch.io/api/convert',
                         headers={'Authorization': 'Bearer d553fad9dd24d7927cd6757a43c40bb7ea2eec02'},
                         json={'source': 'https://www.wikipedia.org/',
                               'margins': {'top': '50px', 'bottom': '50px'},
                               'custom_header': '<header style="width:100%;text-align:center;font-size:16px;">Page'
                                                ' <span class="pageNumber"></span> of <span class="totalPages">'
                                                '</span></header>',
                               'custom_footer': '<footer style="width:100%;text-align:center;font-size:16px;">Date:'
                                                ' <span class="date"></span></footer>'},
                         stream=True)

print(response.status_code)

with open('result.pdf', 'wb') as f:
    for ch in response.iter_content(chunk_size=1024):
        f.write(ch)
