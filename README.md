# TCGPlayerAPISDK
An unofficial python SDK for the TCGPlayer.com API

# Introduction
I started working on this SDK after several months of working with the TCGPlayer API, I wanted to make this for my own personal projects while also helping others make there own projects without stumbling through the API like I did. This is my first major project so any constructive criticism is appreciated.

# Credentials
In order to utilize any of the API endpoints you first need a bearer token. In order to a get bearer token you need a client secret and public from TCGPlayer. These credentials can be applied for at: <br>
http://developer.tcgplayer.com/developer-application-form.html <br>
Once you have credentials you can use the create_bearer_token function to generate your first bearer token, these should be stored carefully as they represent your full access to the API. Each bearer lasts 2 weeks from when issued. You can request a new bearer whenever you want but it is good practice to cache yours locally and only reset it when your old one expires.
