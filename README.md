# solacestack
Tools to setup Solace demo environment

# Quick Start
## Clone
<pre><code>
git clone https://github.com/lik2oxy/solacestack.git 
</code></pre>

## Build 
<pre><code>
docker build --tag solaceansibletest:0.4 .
</code></pre>

## Run
<pre><code>
docker run -v <URI_MY_Proj_ServiceAccount>:/app-pb/res/my-project-serviceaccount.json -p 5000:5000 -it solaceansibletest:0.4
</code></pre>
