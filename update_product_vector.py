from processor import create_data

if __name__ == "__main__":
    df_dir = './data/product_related/'
    ids_path = "./index/products.pkl"
    vector_path = "./index/vectors.index"
    create_data(df_dir,ids_path,vector_path)

