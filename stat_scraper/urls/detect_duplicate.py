def detect_duplicate_urls():
    urlsfile = open('stat_scraper/urls/events_urls.txt')
    urls = urlsfile.read().split(', ')
    urlsfile.close()
    processed_urls = []
    duplicate_indexes = []
    for i, url in enumerate(urls):
        if url in processed_urls:
            duplicate_indexes.append(i)
        processed_urls.append(url)
    return duplicate_indexes


duplicate_urls = detect_duplicate_urls()
print(len(duplicate_urls))