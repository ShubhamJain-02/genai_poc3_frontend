
import './App.css';
import Navbar from './components/Navbar.jsx';
import Home from './pages/Home.jsx';
import Mom from './pages/Mom.jsx';

function App() {
  return (
    <>
    <div className='app'><Navbar/></div>
    <Home/>
    <Mom/>
    </>
  );
}

export default App;
