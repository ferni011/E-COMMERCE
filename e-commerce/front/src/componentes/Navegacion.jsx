import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';

function Navegacion() {
    return (
        <Navbar fixed="top" collapseOnSelect expand="lg" className="bg-body-tertiary justify-content-between align-items-center">
            <Container fluid>
                <Navbar.Brand href="../landing-page">E-tienda</Navbar.Brand>
                <div className="ms-auto d-flex align-items-center">
                    <Form className="d-flex me-3" method="get" action="../busqueda/">
                        <FormControl type="search" name="palabra" placeholder="Search" className="me-2" />
                        <Button type="submit">Search</Button>
                    </Form>

                    <Button href="" className="me-3">Añadir producto</Button>


                    <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                    <Navbar.Collapse id="responsive-navbar-nav" className="justify-content-end">
                        <NavDropdown title="Categorías" id="collapsible-nav-dropdown" className="me-3">
                            <NavDropdown.Item href="">Men's clothing</NavDropdown.Item>
                            <NavDropdown.Item href="">Women's clothing</NavDropdown.Item>
                            <NavDropdown.Item href="">Jewelery</NavDropdown.Item>
                            <NavDropdown.Item href="">Electronics</NavDropdown.Item>
                        </NavDropdown>

                        <Nav className="ms-3">
                            <Nav.Link href="">Iniciar sesión</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </div>
            </Container>
        </Navbar>
    );
}

export default Navegacion;