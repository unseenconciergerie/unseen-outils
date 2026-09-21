/* =============================================================
   UNSEEN. — mouvement (partie JavaScript)
   -------------------------------------------------------------
   Ce fichier fait cinq choses, dans cet ordre :

     1. il signale au style que le JavaScript fonctionne
     2. il compose le nom UNSEEN. lettre par lettre
     3. il empile les trois photos de l'ouverture et les enchaîne
     4. il fait apparaître chaque bloc quand on arrive dessus
     5. il fait apparaître les points de la carte un par un

   Rien ici n'est indispensable au site : si ce fichier est
   retiré ou ne se charge pas, la page reste complète et lisible,
   simplement immobile. C'est voulu, et c'est pour ça que la
   classe "js-anim" n'est posée qu'à la toute première ligne.

   Les styles correspondants sont dans anim.css.
   ============================================================= */

(function(){
  'use strict';

  var doc = document.documentElement;

  /* Le visiteur a-t-il demandé moins d'animations dans les
     réglages de son appareil ? Si oui, on n'anime rien. */
  var sobre = window.matchMedia &&
              window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  doc.classList.add('js-anim');


  /* --------------------------------------------------------- */
  /* 1. Le nom, lettre par lettre                              */
  /* --------------------------------------------------------- */

  function composerLogo(){
    var mark = document.querySelector('.hero-mark');
    if (!mark) return;

    var nom = mark.textContent.trim();          /* "UNSEEN." */
    mark.textContent = '';
    /* Le nom est découpé en autant de petites boîtes. Pour un
       lecteur d'écran ce découpage n'existe pas : il lit
       l'étiquette posée ici et ignore les lettres une à une. */
    mark.setAttribute('aria-label', nom);

    for (var i = 0; i < nom.length; i++){
      var lettre = document.createElement('span');
      var estPoint = nom[i] === '.';
      lettre.className = estPoint ? 'ltr pt' : 'ltr';
      lettre.textContent = nom[i];
      lettre.setAttribute('aria-hidden', 'true');
      /* Les lettres montent l'une après l'autre, puis le point
         arrive seul après un silence : c'est lui qui signe. */
      lettre.style.animationDelay = (estPoint ? 0.62 : i * 0.075) + 's';
      mark.appendChild(lettre);
    }
  }


  /* --------------------------------------------------------- */
  /* 2. L'ouverture : trois photos qui se relaient             */
  /* --------------------------------------------------------- */

  var AUTRES_PHOTOS = ['hero-2', 'hero-3'];
  var DUREE_PHOTO = 8000;      /* huit secondes par photo */

  function composerOuverture(){
    var hero = document.querySelector('.hero');
    /* Le cadre existe déjà dans la page : on ne fait qu'y ajouter les
       photos suivantes. Ainsi, si ce script n'arrive jamais jusqu'au
       visiteur, la première photo reste en place et bien derrière le
       texte, au lieu de se ranger à côté de lui. */
    var cadre = hero && hero.querySelector('.hero-bg');
    if (!hero || !cadre) return;

    AUTRES_PHOTOS.forEach(function(nom){
      var bloc = document.createElement('picture');
      bloc.className = 'hslide';
      var avif = document.createElement('source');
      avif.type = 'image/avif';
      avif.srcset = 'img/' + nom + '.avif';
      var img = document.createElement('img');
      img.src = 'img/' + nom + '.webp';
      img.alt = '';
      img.loading = 'lazy';
      img.decoding = 'async';
      bloc.appendChild(avif);
      bloc.appendChild(img);
      cadre.appendChild(bloc);
    });

    /* Le repère de défilement, en bas de l'écran d'ouverture */
    var repere = document.createElement('div');
    repere.className = 'hero-scroll';
    repere.setAttribute('aria-hidden', 'true');
    hero.appendChild(repere);

    if (sobre) return;

    var photos = cadre.querySelectorAll('.hslide');
    var active = 0;
    setInterval(function(){
      /* On ne travaille pas pendant que l'onglet est en arrière-plan */
      if (document.hidden) return;
      photos[active].classList.remove('is-on');
      active = (active + 1) % photos.length;
      photos[active].classList.add('is-on');
    }, DUREE_PHOTO);
  }


  /* --------------------------------------------------------- */
  /* 3. Les blocs apparaissent quand on arrive dessus          */
  /* --------------------------------------------------------- */

  /* Les enfants d'une même rangée arrivent l'un après l'autre.
     Ce décalage se règle ici, en millièmes de seconde. */
  var DECALAGE = 90;
  var DECALAGE_MAX = 6;        /* au-delà, l'attente se verrait */

  var GROUPES = '.cards .card, .dests .dest, .srow .sitem, ' +
                '.mosaic figure, .timeline .tl-step';

  function fairApparaitre(){
    var blocs = document.querySelectorAll('.reveal');
    if (!blocs.length) return;

    /* Pas de guetteur disponible, ou visiteur en mode sobre :
       on montre tout, tout de suite. */
    if (sobre || !('IntersectionObserver' in window)){
      for (var i = 0; i < blocs.length; i++) blocs[i].classList.add('is-in');
      return;
    }

    var guetteur = new IntersectionObserver(function(entrees){
      entrees.forEach(function(e){
        if (!e.isIntersecting) return;
        var bloc = e.target;
        bloc.classList.add('is-in');

        var enfants = bloc.querySelectorAll(GROUPES);
        for (var k = 0; k < enfants.length; k++){
          var rang = Math.min(k, DECALAGE_MAX);
          enfants[k].style.transitionDelay = (rang * DECALAGE) + 'ms';
        }
        /* Une fois le bloc apparu, on cesse de le surveiller :
           il ne se rejoue pas si on remonte la page. */
        guetteur.unobserve(bloc);
      });
    }, {
      /* On déclenche un peu avant que le bloc touche le bas de
         l'écran, pour que le mouvement soit déjà fini quand
         l'œil arrive dessus. */
      rootMargin: '0px 0px -12% 0px',
      threshold: 0.08
    });

    for (var j = 0; j < blocs.length; j++) guetteur.observe(blocs[j]);
  }


  /* --------------------------------------------------------- */
  /* 4. La carte : les points se posent un par un              */
  /* --------------------------------------------------------- */

  function animerCarte(){
    var scene = document.getElementById('mapstage');
    if (!scene) return;

    /* Les points de la destination affichée sont peints à la
       couleur d'accent par le script de la carte. On les
       reconnaît à cette couleur, et on les fait respirer. */
    function marquerLesActifs(){
      var accent = (getComputedStyle(doc).getPropertyValue('--accent') || '').trim().toLowerCase();
      if (!accent) return;
      var points = scene.querySelectorAll('path.leaflet-interactive');
      for (var i = 0; i < points.length; i++){
        var couleur = (points[i].getAttribute('fill') || '').trim().toLowerCase();
        points[i].classList.toggle('pt-actif', couleur === accent);
      }
    }

    /* La carte met un instant à se dessiner : on laisse Leaflet
       poser ses points avant de les faire apparaître. */
    function allumer(){
      scene.classList.add('pts-on');
      marquerLesActifs();
    }

    if (sobre || !('IntersectionObserver' in window)){
      allumer();
    } else {
      var guetteur = new IntersectionObserver(function(entrees){
        if (!entrees[0].isIntersecting) return;
        var points = scene.querySelectorAll('path.leaflet-interactive');
        for (var i = 0; i < points.length; i++){
          points[i].style.transitionDelay = Math.min(i * 28, 900) + 'ms';
        }
        allumer();
        guetteur.disconnect();
      }, {threshold: 0.15});
      guetteur.observe(scene);
    }

    /* Changer de destination repeint les points : on réévalue
       lesquels sont actifs, une fois le repeint terminé. */
    function reevaluer(){ setTimeout(marquerLesActifs, 260); }
    var onglets = document.getElementById('maptabs');
    if (onglets) onglets.addEventListener('click', reevaluer);
    scene.addEventListener('click', reevaluer);
    var carte = document.getElementById('mapcard');
    if (carte) carte.addEventListener('click', reevaluer);
  }


  /* --------------------------------------------------------- */
  /* Mise en route                                             */
  /* --------------------------------------------------------- */

  function demarrer(){
    composerLogo();
    composerOuverture();
    fairApparaitre();
    /* La carte se construit dans un autre script, juste avant
       celui-ci : on lui laisse le temps de poser ses points. */
    setTimeout(animerCarte, 600);
  }

  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', demarrer);
  } else {
    demarrer();
  }
})();
