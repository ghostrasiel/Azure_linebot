
import os
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential

def formrecognizer_by_local(local_image_path):
    # Set user key, endpoint
    key = "55334d079b9949739f108b11dbee454b"
    endpoint = r"https://formtfb1024.cognitiveservices.azure.com/"

    # call API
    form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
    trained_model_id = ""

    # image location
    # local_image_path = os.getcwd() + '/photo/test/test__42385416.jpg'

    # 讀取圖片 (二進位)
    local_image = open(local_image_path, "rb")

    poller = form_recognizer_client.begin_recognize_custom_forms(model_id=trained_model_id, form=local_image)
    result = poller.result()

    output = {}


    for recognized_form in result:
        print("Form type: {}".format(recognized_form.form_type))
        print(recognized_form.fields)
        print('---------------------')
        for name, field in recognized_form.fields.items():
            if name not in output:
                output[name]= str(field.value)
            else:
                output[name].append(field.value)
    
    output["年份"] = output["年"][0:3]
    output["月份"] = output["月"].split('-')[0].zfill(2)
    output["發票號碼"] = output["號碼"][-8:]
    output["日期"] = output["年份"][0:3]+output["月份"].split('-')[0].zfill(2)
    return output
    
# if __name__ == '__main()__':
#     formrecognizer_by_local(local_image_path)


# local_image_path = "C:\\Users\\Tibame_25\\Desktop\\Line_bot\\發票模組訓練\\測試\\S__19996689.jpg"
# print(formrecognizer_by_local(local_image_path))

