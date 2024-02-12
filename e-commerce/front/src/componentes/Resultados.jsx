import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Rating } from 'primereact/rating';
import 'primereact/resources/themes/saga-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function Resultados() {
  const [productos, setProductos] = useState([]);
  let token = "root";
  const query = useQuery();
  const palabra = query.get('palabra'); 

  useEffect(() => {
    fetch('http://localhost:8000/api/productos?desde=0&hasta=400', {
      headers: {
        'Authorization': `Bearer ${token}`, 
      }
    })
      .then(response => response.json())
      .then(data => {
        let productosFiltrados = data;
        if (palabra) {
          const palabraEnMinuscula = palabra.toLowerCase();
          productosFiltrados = data.filter(producto =>
            producto.title.toLowerCase().includes(palabraEnMinuscula) ||
            producto.description.toLowerCase().includes(palabraEnMinuscula) ||
            producto.category.toLowerCase().includes(palabraEnMinuscula)
          );
        }
        setProductos(productosFiltrados);
      })
      .catch(error => console.error(error));
  }, [palabra]);

  return (
    <div className="container mt-5">
      <div className="row">
        {productos.length > 0 ? (
          productos.map((producto, index) => (
            <div className="col-md-4 d-flex align-items-stretch" key={producto.id}>
              <div className="card mb-3">
                <img src={`http://localhost:8000/static/${producto.image}`} className="card-img-top img-custom-size" alt={producto.title} style={{ height: '450px', width: '100%'  }} />
                <div className="card-body d-flex flex-column">
                  <div className="flex-grow-1">
                    <h5 className="card-title mb-auto">
                      <p data-title={producto.title}>{producto.title}</p>
                    </h5>
                    <h5 className="card-subtitle mt-2 font-weight-bold">€ {producto.price}</h5>
                    <Rating value={producto.rating.rate} readOnly stars={5} cancel={false} style={{ color: 'blue', marginLeft: '85px', marginTop: '40px' }} fraction={2} />
                    <span className="sp" data-product-id={producto.id}></span>
                  </div>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div>No se encontraron resultados</div>
        )}
      </div>
    </div>
  );
}

export default Resultados;