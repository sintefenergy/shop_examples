FROM shopacrbinderhub.azurecr.io/shop/shop_jupyterlab_default:latest

RUN pip install --no-cache-dir vdom==0.5
