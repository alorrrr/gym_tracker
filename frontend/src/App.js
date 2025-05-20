// App.js
import './index.css';
import React, { useState, useEffect, useCallback } from "react";
import { 
  BrowserRouter as Router, 
  Route, 
  Routes, 
  Navigate,
  useNavigate, // Добавить
  Link // Добавить
} from "react-router-dom";

// API Endpoints
const API_BASE = "http://127.0.0.1/api";

const Navbar = ({ onLogout }) => {
  return (
    <nav className="bg-[#1877f2] fixed w-full top-0 left-0 z-50 shadow-md py-3">
      <div className="max-w-2xl mx-auto px-4 flex justify-between items-center">
        <h1 className="text-white text-xl font-bold">Workout Tracker</h1>
        <button 
          onClick={onLogout}
          className="flex items-center gap-1 bg-white/10 hover:bg-white/20 text-white px-3 py-1 rounded-md transition-colors text-sm"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          Выход
        </button>
      </div>
    </nav>
  );
};


const Registration = ({ onRegistration }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateEmail(email)) {
      setError('Некорректный email адрес');
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/auth/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, email }),
      });

      if (response.ok) {
        alert('Письмо с подтверждением отправлено на вашу почту');
        navigate('/login');
      } else {
        const data = await response.json();
        setError(data.message || 'Ошибка регистрации');
      }
    } catch (err) {
      setError('Ошибка соединения с сервером');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">Registration</h2>
      <form className="space-y-4" onSubmit={handleSubmit}>
        {error && <div className="text-red-500 text-sm">{error}</div>}
        
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-[#1877f2]"
          required
        />
        
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-[#1877f2]"
          required
        />
        
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-[#1877f2]"
          required
        />
        
        <button
          type="submit"
          className="w-full bg-[#42b72a] text-white py-3 rounded-lg font-semibold hover:bg-[#36a420] transition-colors"
        >
          Sign up
        </button>
        
        <div className="text-center mt-4">
          <span className="text-gray-600">Already have an account? </span>
          <Link to="/login" className="text-[#1877f2] hover:underline">
            Login
          </Link>
        </div>
      </form>
    </div>
  );
};


const Auth = ({ onAuth }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleAuth = (isLogin) => async (event) => {
    event.preventDefault();
    const endpoint = isLogin ? "token/login/" : "";
    
    try {
      const response = await fetch(`${API_BASE}/auth/${endpoint}`, {
        method: "POST",
        body: JSON.stringify({ username, password }),
        headers: { "Content-Type": "application/json" },
      });

      if (response.ok) {
        if (isLogin) {
          const data = await response.json();
          const token = data.auth_token;
          localStorage.setItem("token", token);

          const userResponse = await fetch(`${API_BASE}/auth/me`, {
            headers: { Authorization: `Token ${token}` },
          });

          if (userResponse.ok) {
            const userData = await userResponse.json();
            localStorage.setItem("user_id", userData.id);
            onAuth(true);
          }
        } else {
          alert("Registration successful. You can now log in.");
        }
      } else {
        alert(isLogin ? "Login failed." : "Registration failed.");
      }
    } catch (error) {
      console.error("Auth error:", error);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">Workout Tracker</h2>
      <form className="space-y-4">
        <input
          type="text"
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-[#1877f2]"
        />
        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-[#1877f2]"
        />
        <button 
        onClick={handleAuth(true)} // ✅ Теперь передается функция
        className="w-full bg-[#1877f2] text-white py-3 rounded-lg font-semibold hover:bg-[#166fe5] transition-colors"
      >
        Log In
      </button>
        <div className="text-center my-4">
          <hr className="border-gray-300" />
          <span className="bg-white px-2 text-gray-500 -mt-3 inline-block">or</span>
        </div>
        <Link to="/register" className="text-[#1877f2] hover:underline">
          Sign up
        </Link>
      </form>
    </div>
  );
};

const AddWorkout = ({ onAdd }) => {
  const [duration, setDuration] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    const userId = localStorage.getItem("user_id");
    
    if (userId) {
      const response = await fetch(`${API_BASE}/trainings/`, {
        method: "POST",
        body: JSON.stringify({ user_id: userId, duration: parseInt(duration) || 0 }),
        headers: { "Content-Type": "application/json" },
      });

      if (response.ok) {
        const newWorkout = await response.json();
        onAdd(newWorkout);
        setDuration("");
      }
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <h3 className="text-lg font-semibold mb-4">Create New Workout</h3>
      <form onSubmit={handleSubmit} className="flex gap-4">
        <input
          type="number"
          placeholder="Duration (minutes)"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-[#1877f2]"
        />
        <button 
          type="submit" 
          className="bg-[#1877f2] text-white px-6 py-2 rounded-lg hover:bg-[#166fe5] transition-colors"
        >
          Add
        </button>
      </form>
    </div>
  );
};

const AddExercise = ({ workoutId, onAdd }) => {
  const [formData, setFormData] = useState({
    name: "",
    sets: "",
    reps: "",
    weight: "",
    rest: ""
  });

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch(`${API_BASE}/exercises/`, {
      method: "POST",
      body: JSON.stringify({
        ...formData,
        sets: parseInt(formData.sets),
        reps: parseInt(formData.reps),
        weight: parseFloat(formData.weight),
        rest: parseInt(formData.rest),
        training_id: workoutId
      }),
      headers: { "Content-Type": "application/json" },
    });

    if (response.ok) {
      const newExercise = await response.json();
      onAdd(newExercise);
      setFormData({ name: "", sets: "", reps: "", weight: "", rest: "" });
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <h3 className="text-lg font-semibold mb-4">Add Exercise</h3>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
        <input
          type="text"
          placeholder="Exercise name"
          value={formData.name}
          onChange={(e) => setFormData({...formData, name: e.target.value})}
          className="col-span-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-[#1877f2]"
        />
        <input
          type="number"
          placeholder="Sets"
          value={formData.sets}
          onChange={(e) => setFormData({...formData, sets: e.target.value})}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-[#1877f2]"
        />
        <input
          type="number"
          placeholder="Reps"
          value={formData.reps}
          onChange={(e) => setFormData({...formData, reps: e.target.value})}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-[#1877f2]"
        />
        <input
          type="number"
          placeholder="Weight (kg)"
          value={formData.weight}
          onChange={(e) => setFormData({...formData, weight: e.target.value})}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-[#1877f2]"
        />
        <input
          type="number"
          placeholder="Rest (min)"
          value={formData.rest}
          onChange={(e) => setFormData({...formData, rest: e.target.value})}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-[#1877f2]"
        />
        <button 
          type="submit"
          className="col-span-2 bg-[#1877f2] text-white py-2 rounded-lg hover:bg-[#166fe5] transition-colors"
        >
          Add Exercise
        </button>
      </form>
    </div>
  );
};

const WorkoutDetails = ({ workout, onExerciseAdded, onWorkoutDeleted }) => {
  const [exercises, setExercises] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  const fetchExercises = useCallback(async () => {
    const response = await fetch(`${API_BASE}/exercises/?training_id=${workout.id}`);
    if (response.ok) setExercises(await response.json());
  }, [workout.id]);

  useEffect(() => { fetchExercises(); }, [fetchExercises]);

  const formatDate = (dateString) => {
    const options = { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
    };
    return new Date(dateString).toLocaleDateString('ru-RU', options);
  };

  const handleDeleteExercise = async (exerciseId) => {
    if (window.confirm("Вы уверены, что хотите удалить это упражнение?")) {
      console.log(exerciseId)
      const response = await fetch(`${API_BASE}/exercises/${exerciseId}/`, {
        method: "DELETE",
      });

      if (response.ok) {
        fetchExercises();
      }
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <div className="flex justify-between items-center cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
        <div>
          <h3 className="font-semibold text-lg">Workout</h3>
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <span>{formatDate(workout.date)}</span>
            {workout.duration > 0 && (
              <span className="flex items-center gap-1">
                ⏱️ {workout.duration} мин
              </span>
            )}
          </div>
        </div>
        <button
            onClick={(e) => {
              e.stopPropagation();
              onWorkoutDeleted();
            }}
            className="text-red-500 hover:text-red-700 p-1 rounded-full hover:bg-red-50"
          >
            🗑️
        </button>
        <span className={`transform transition-transform ${isOpen ? 'rotate-180' : ''}`}>▼</span>
      </div>
      
      {isOpen && (
        <div className="mt-4">
          <AddExercise workoutId={workout.id} onAdd={() => { fetchExercises(); onExerciseAdded(); }} />
          <div className="mt-4 space-y-3">
            {exercises.map(exercise => (
              <div key={exercise.id} className="border-t pt-3">
                <p className="font-medium">{exercise.name}</p>
                <div className="grid grid-cols-4 gap-2 text-sm text-gray-600">
                  <span>{exercise.sets} sets</span>
                  <span>{exercise.reps} reps</span>
                  <span>{exercise.weight} kg</span>
                  <span>{exercise.rest} min rest</span>
                </div>
                
                <button 
                  onClick={() => handleDeleteExercise(exercise.id)}
                  className="text-blue-500 hover:text-red-700 ml-4"
                >
                ✕
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const CreateWorkout = ({ onLogout }) => {
  const [workouts, setWorkouts] = useState([]);

  const fetchWorkouts = async () => {
    const response = await fetch(`${API_BASE}/trainings/`, {
      headers: { Authorization: `Token ${localStorage.getItem("token")}` },
    });
    if (response.ok) setWorkouts(await response.json());
  };

  const handleDeleteWorkout = async (workoutId) => {
    if (window.confirm("Вы уверены, что хотите удалить всю тренировку?")) {
      const response = await fetch(`${API_BASE}/trainings/${workoutId}/`, {
        method: "DELETE",
        headers: { Authorization: `Token ${localStorage.getItem("token")}` },
      });

      if (response.ok) {
        fetchWorkouts();
      }
    }
  };

  useEffect(() => { fetchWorkouts(); }, []);

  return (
    <div className="pt-16">
      <Navbar onLogout={() => {
        localStorage.removeItem("token");
        localStorage.removeItem("user_id");
        onLogout(false);
      }} />
      <div className="max-w-2xl mx-auto px-4">
        <AddWorkout onAdd={() => fetchWorkouts()} />
        <div className="space-y-4">
          {workouts.map(workout => (
            <WorkoutDetails 
              key={workout.id}
              workout={workout}
              onExerciseAdded={fetchWorkouts}
              onWorkoutDeleted={() => handleDeleteWorkout(workout.id)}
            />
          ))}
        </div>
      </div>
      
    </div>
  );
};

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem("token"));

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Routes>
          <Route path="/login" element={isAuthenticated ? <Navigate to="/workouts" /> : <Auth onAuth={setIsAuthenticated} />} />
          <Route path="/register" element={isAuthenticated ? <Navigate to="/workouts" /> : <Registration />} />
          <Route path="/workouts" element={
            isAuthenticated 
              ? <CreateWorkout onLogout={() => setIsAuthenticated(false)} /> 
              : <Navigate to="/login" />
          } />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;