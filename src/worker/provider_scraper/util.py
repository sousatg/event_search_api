def get_element(doc, xpath):
    element_list = doc.xpath(xpath)

    if element_list and len(element_list) > 0:
        return element_list[0]
    else:
        raise Exception(f'Missing element: {xpath}')
