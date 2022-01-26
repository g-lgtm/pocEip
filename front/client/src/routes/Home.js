import React from "react";
import Field from '../components/Field'


const Home = () => {
    const healthfield = 96;
    return (
        <div>
            <div className="bg_home">
                <img src="./img/bg.jpeg" alt="bghome"/>
                <h1>Bienvenue sur Flylens</h1>
                <h2>Commencer à analyser les champs</h2>
                <a href="#analyse-section">
                    <div class="container">
                      <div class="content">
                        <svg id="more-arrows">
                          <polygon class="arrow-top" points="37.6,27.9 1.8,1.3 3.3,0 37.6,25.3 71.9,0 73.7,1.3 "/>
                          <polygon class="arrow-middle" points="37.6,45.8 0.8,18.7 4.4,16.4 37.6,41.2 71.2,16.4 74.5,18.7 "/>
                          <polygon class="arrow-bottom" points="37.6,64 0,36.1 5.1,32.8 37.6,56.8 70.4,32.8 75.5,36.1 "/>
                        </svg>
                      </div>
                    </div>
                </a>    
            </div>
            <div id="analyse-section">
                <div class="left-section">
                    <h3>Graphique d'analyse des champs:</h3>
                    <p>La moyenne de vert des champs analysés est de {healthfield} %.</p>
                    <p>Vos plantations sont en bonne santé.</p>
                    <p>Pour avoir plus de detail sur chaque champ selectionnez en un.</p>
                    <Field />
                </div>
                <div class="right-section">
                    <div class="button_field">
                        <button>Tous les champs</button>
                        <button>Champ 1</button>
                        <button>Champ 2</button>
                        <button>Champ 3</button>
                    </div>
                    <img src="./img/mais.jpeg" alt="img_field"/>
                </div>
                
            </div>
        </div>
    );
};

export default Home;