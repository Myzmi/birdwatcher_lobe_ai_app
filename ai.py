from predict_library import predict_label_from_url

url = input("Enter image URL: ")
predicted_label = predict_label_from_url(url)
print(f"Predicted label: {predicted_label}")