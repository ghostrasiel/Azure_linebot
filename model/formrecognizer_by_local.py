#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# by local

def formrecognizer_by_local(local_image_path):
    import os
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.formrecognizer import FormRecognizerClient
    from azure.ai.formrecognizer import FormTrainingClient
    from azure.core.credentials import AzureKeyCredential

    # Set user key, endpoint
    key = "653310d794cd4bcba674b91918a7dc72"
    endpoint = "https://tfb102-t4-project.cognitiveservices.azure.com/"

    # call API
    form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
    trained_model_id = "240e58da-7514-4e22-9ac4-efd6705d8280"

    # image location
#     local_image_path = os.getcwd() + '/photo/test/test__42385416.jpg'

    # 讀取圖片 (二進位)
    local_image = open(local_image_path, "rb")

    poller = form_recognizer_client.begin_recognize_custom_forms(model_id=trained_model_id, form=local_image)
    result = poller.result()

    output = {}


    for recognized_form in result:
        print("Form type: {}".format(recognized_form.form_type))
    #     print(recognized_form.fields)
        for name, field in recognized_form.fields.items():
            if name not in output:
                output[name]= str(field.value)
            else:
                output[name].append(field.value)

    output["年份"] = output["年份"].replace(' 年','')
    output["月份"] = output["月份"].replace(' 月','').replace('-','')
    output["發票號碼"] = output["發票號碼"][-8:]
    output["日期"] = output["年份"]+output["月份"]
    print(output)
    
if __name__ == '__main()__':
    formrecognizer_by_local(local_image_path)

