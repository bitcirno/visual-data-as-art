[//]: # (Reference: https://github.com/Rostave/Best-README-Template by othneildrew)
<a id="readme-top"></a>
<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">SD5913 CREATIVE PROGRAMMING FOR DESIGNERS AND ARTISTS</h3>

  <p align="center">
    Assignment 2 - Data Visulization - Tropical Cyclone Calendar
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<!-- <details> -->
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
<!-- </details> -->

-------------------


<!-- ABOUT THE PROJECT -->
## About The Project

![demo_img1](repo_img/demo_img1.png)
![demo_img1](repo_img/demo_img2.png)
![tc)types_img](repo_img/tc-types.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Tropical Cyclone Calendar

The Tropical Cyclone Calendar (TCC) is an interactive data visualization application 
designed to present historical records of tropical cyclones (TCs) based on data from
the Hong Kong Observatory (HKO). Built with Python and Pygame, and enhanced by Pygame Shaders, 
TCC offers an engaging and intuitive way to explore the occurrence and severity of 
tropical cyclones throughout the year.

### Visual Design and Features

* **Calendar View.**
At the bottom of the interface, a row of circular nodes represents the days of the selected month. 
Each node acts as a date button. The size of each node visually encodes the severity of the tropical 
cyclone recorded on that day—the more severe the TC, the larger the node. This allows users to quickly 
identify significant events at a glance.


* **Interactive Exploration.**
Hovering your pointer over a date node reveals detailed information about the tropical cyclone that 
occurred on that day. The left side of the screen displays the cyclone’s name (in both Chinese and English) 
and its classification (e.g., Super Typhoon, Severe Tropical Storm). The right side provides additional details, 
such as the warning signal issued and its timing.


* **Dynamic Background Simulation.**
The background of the application features a real-time, shader-based simulation of a tropical cyclone.
This swirling visual effect not only enhances the atmosphere but also provides a contextual illustration of the 
cyclone’s intensity and structure, making the data more immersive.


* **Month Navigation.**
Users can scroll the mouse wheel or use the PageUp and PageDown keys to switch between months, 
allowing for easy browsing of past tropical cyclone records.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org)
* [Pygame](https://www.pygame.org/news) for application developing
* [Pygame Shaders](https://github.com/ScriptLineStudios/pygame_shaders) for TC shader visualization


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

You may run the app by the following steps.

### Prerequisites
  ```sh
  pip install -r requirements.txt
  ```
_Of course you can use other package management tools!_

### Running
```sh
python main.py
```
_Now you may wait for the visualization window to launch which may take a few seconds to request data online._

If everything goes well, you will see the output in terminal as shown below:
```
[App]    Launched with resolution: (960, 540), FPS: 60
[Data]   Fetching data from HKO...
[Data]   Fetched the latest tropical cyclone records from HKO
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

You may see two contributors, both of them are mine. Github makes multi-device development easy!
### Top contributors:

<a href="https://github.com/bitcirno/visual-data-as-art/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=bitcirno/visual-data-as-art" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Unlicensed currently.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

bitCirno (Bilibili) - [@Rostave](https://b23.tv/3oXghzO) - 1637131272@qq.com

Project Link: [https://github.com/bitcirno/visual-data-as-art](https://github.com/bitcirno/visual-data-as-art)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [香港天文台](https://www.hko.gov.hk/tc/informtc/tcMain.htm)
* [Pygame](https://www.pygame.org/news)
* [Pygame Shaders](https://github.com/ScriptLineStudios/pygame_shaders)
* [GitHub Pages](https://pages.github.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/bitcirno/visual-data-as-art.svg?style=for-the-badge
[contributors-url]: https://github.com/bitcirno/visual-data-as-art/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/bitcirno/visual-data-as-art.svg?style=for-the-badge
[forks-url]: https://github.com/bitcirno/visual-data-as-art/network/members
[stars-shield]: https://img.shields.io/github/stars/bitcirno/visual-data-as-art.svg?style=for-the-badge
[stars-url]: https://github.com/bitcirno/visual-data-as-art/stargazers
[issues-shield]: https://img.shields.io/github/issues/bitcirno/visual-data-as-art.svg?style=for-the-badge
[issues-url]: https://github.com/bitcirno/visual-data-as-art/issues
[license-shield]: https://img.shields.io/github/license/bitcirno/visual-data-as-art.svg?style=for-the-badge
[license-url]: https://github.com/bitcirno/visual-data-as-art/blob/master/LICENSE.txt

