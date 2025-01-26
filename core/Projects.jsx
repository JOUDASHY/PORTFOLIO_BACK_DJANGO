import React, { useEffect, useState } from "react";
import axios from "axios";

const Projects = () => {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    // Récupérer les données de l'API
    const fetchProjects = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/projets/");
        setProjects(response.data);
      } catch (error) {
        console.error("Erreur lors du chargement des projets :", error);
      }
    };

    fetchProjects();
  }, []);

  return (
    <div>
      {/* Navbar */}
   

      {/* Projects Section */}
      <section className="work" id="work">
        <h2 className="heading">
          <i className="fas fa-laptop-code"></i> Projects <span>Made</span>
        </h2>

        <div className="box-container">
          {projects.map((project) => (
            <div className="box tilt" key={project.id}>
              <img
                src={
                  project.related_images.length > 0
                    ? project.related_images[0].image
                    : "/assets/images/projects/default.png"
                }
                alt={project.nom}
              />
              <div className="content">
                <div className="tag">
                  <h3>{project.nom}</h3>
                </div>
                <div className="desc">
                  <p>{project.description}
                  {project.average_score ? (
                      <>
                        {renderStars(project.average_score, false, project.id)} (
                        {project.average_score.toFixed(1)}/5)
                      </>
                    ) : (
                      "Pas encore noté"
                    )}

                  </p>
                  <p><strong>Technologies:</strong> {project.techno}</p>
                  <div className="rating">
                  <p><strong>Donnez une note :</strong></p>
                  <div>{renderStars(selectedScore[project.id] || 0, true, project.id)}</div>
                  <button
                    className="btn btn-primary mt-2"
                    onClick={() => handleRatingSubmit(project.id)}
                    disabled={loading}
                  >
                    {loading ? "En cours..." : "Noter"}
                  </button>
                </div>

                  <div className="btns">
                    <a href="#" className="btn" target="_blank" rel="noopener noreferrer">
                      <i className="fas fa-eye"></i> View
                    </a>
                    <a href="#" className="btn" target="_blank" rel="noopener noreferrer">
                      Code <i className="fas fa-code"></i>
                    </a>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="backbtn">
          <a href="/#work" className="btn">
            <i className="fas fa-arrow-left"></i>
            <span>Back to Home</span>
          </a>
        </div>
      </section>

      {/* Scroll Top Button */}
      <a href="#work" className="fas fa-angle-up" id="scroll-top"></a>
    </div>
  );
};

export default Projects;
