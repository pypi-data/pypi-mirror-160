def save_model(clf, file_name: str, prefix: str, ending=".bee") -> dict:
    file_name = make_full_file_name(file_name=file_name, prefix=prefix)
    clf.save()
