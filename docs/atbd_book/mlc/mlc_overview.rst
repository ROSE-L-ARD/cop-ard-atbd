.. _mlc_overview:

==========================================
Overview
==========================================

The MLC product is a multi-looked ARD product suited to large-scale interferometric applications. It is inspired by intermediate products which are normally present in PS/DS and SBAS chains before phase unwrapping (:cite:author:`Teba2008,Fornaro2015,Ansari2018,Pepe2019`). For the ROSE-L missions the proposed resolution of this product is 50 m.

The MLC product is intended to simplify the access to interferometric measurements which are usually quite unaccessible: the product has reduced noise compared to full-resolution interferograms as it is already multilooked, it is generated with a mechanism to minimize long-term phase drifts related to vegetation effects, and it has a much smaller size compared to the original CSLC stack. The product is first generated in radar coordinates on a sub-sampling of the original SLC grid. Because of this, this version is called CMLC (Co-registered Multi-looked Complex). Its final version after geocoding is called GMLC.

There are different approaches in the literature to generate such product. Here we describe an algorithm which exhibits the following characteristics:

- it is very lightweight in terms of data I/O and computation,
- it enables continuous product update as new images are acquired and the CLSC stack grows,
- it incorporates a long-term drift correction.
