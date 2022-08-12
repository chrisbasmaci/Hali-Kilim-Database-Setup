--------------------------Q1-----------------------------------------------------------------------
SELECT kilimler.k_key, origin, width, length, m2, price, photos.link
from kilimler
INNER JOIN photos ON kilimler.k_key = photos.k_key
ORDER BY price DESC
---Fiyatlari yuksekten dusuge gore siralanmis sekilde kilimlerin bilgilerini ve fotograflarini veriyor---
--------------------------Q2----------------------------------------------------------------------
SELECT halilar.h_key, origin, width, length, m2, price, photos.link
from halilar
INNER JOIN photos ON halilar.h_key = photos.h_key
ORDER BY price DESC
---Fiyatlari yuksekten dusuge gore siralanmis sekilde halilarin bilgilerini ve fotograflarini veriyor---
