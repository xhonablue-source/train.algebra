import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Calculator, Zap } from 'lucide-react';

const TrainCalculator = () => {
  const [scenario, setScenario] = useState('same-direction');
  const [isAnimating, setIsAnimating] = useState(false);
  const [animationTime, setAnimationTime] = useState(0);
  const [trainASpeed, setTrainASpeed] = useState(40);
  const [trainBSpeed, setTrainBSpeed] = useState(60);
  const [headStart, setHeadStart] = useState(2);
  const [showCalculations, setShowCalculations] = useState(false);
  const animationRef = useRef();

  const calculateMeeting = () => {
    if (scenario === 'same-direction') {
      if (trainBSpeed <= trainASpeed) return null;
      const meetingTime = (trainASpeed * headStart) / (trainBSpeed - trainASpeed);
      const meetingDistance = trainBSpeed * meetingTime;
      return { 
        time: meetingTime, 
        distance: meetingDistance,
        trainADistance: trainASpeed * (meetingTime + headStart),
        trainBDistance: trainBSpeed * meetingTime 
      };
    } else {
      const combinedSpeed = trainASpeed + trainBSpeed;
      const initialDistance = trainASpeed * headStart;
      const meetingTime = initialDistance / combinedSpeed;
      const meetingDistance = trainASpeed * (headStart + meetingTime);
      return { 
        time: meetingTime, 
        distance: meetingDistance,
        trainADistance: trainASpeed * (headStart + meetingTime),
        trainBDistance: trainBSpeed * meetingTime
      };
    }
  };

  const meeting = calculateMeeting();

  useEffect(() => {
    if (isAnimating) {
      const startTime = Date.now();
      const animate = () => {
        const elapsed = (Date.now() - startTime) / 1000;
        setAnimationTime(elapsed);
        
        if (meeting && elapsed < meeting.time + 3) {
          animationRef.current = requestAnimationFrame(animate);
        } else {
          setIsAnimating(false);
        }
      };
      animationRef.current = requestAnimationFrame(animate);
    }
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isAnimating, meeting]);

  const resetAnimation = () => {
    setIsAnimating(false);
    setAnimationTime(0);
  };

  const getTrainPositions = () => {
    const trackWidth = 700;
    const maxDistance = meeting ? Math.max(meeting.distance * 1.3, 300) : 300;
    
    let trainADistance, trainBDistance;
    
    if (scenario === 'same-direction') {
      trainADistance = trainASpeed * (animationTime + headStart);
      trainBDistance = animationTime > 0 ? trainBSpeed * animationTime : 0;
    } else {
      trainADistance = trainASpeed * (animationTime + headStart);
      trainBDistance = animationTime > 0 ? trainBSpeed * animationTime : 0;
    }
    
    const trainAPos = Math.min((trainADistance / maxDistance) * trackWidth, trackWidth - 100);
    let trainBPos;
    
    if (scenario === 'same-direction') {
      trainBPos = Math.min((trainBDistance / maxDistance) * trackWidth, trackWidth - 100);
    } else {
      trainBPos = Math.max(trackWidth - 100 - (trainBDistance / maxDistance) * trackWidth, 0);
    }
    
    return { trainAPos, trainBPos, maxDistance, trainADistance, trainBDistance };
  };

  const { trainAPos, trainBPos, maxDistance, trainADistance, trainBDistance } = getTrainPositions();

  // Jet-Powered Super Train Component
  const JetSuperTrain = ({ type, direction, speed, distance, label, isActive, onClick, scenario }) => {
    const isHyperloop = type === 'hyperloop';
    const isReversed = direction === 'left';
    
    return (
      <div 
        className={`relative cursor-pointer transform transition-all duration-500 hover:scale-110 ${
          isActive ? 'scale-105 drop-shadow-2xl' : 'hover:scale-105'
        }`}
        onClick={onClick}
      >
        {/* Glow effect when active */}
        {isActive && (
          <div className={`absolute inset-0 rounded-2xl blur-xl opacity-75 ${
            isHyperloop ? 'bg-blue-400' : 'bg-purple-400'
          }`}></div>
        )}
        
        <div className={`relative flex items-center ${isReversed ? 'flex-row-reverse' : ''} p-6 rounded-2xl border-4 transition-all duration-300 ${
          isActive 
            ? (isHyperloop ? 'border-blue-400 bg-blue-50 shadow-2xl' : 'border-purple-400 bg-purple-50 shadow-2xl')
            : 'border-gray-300 bg-white hover:border-gray-400'
        }`}>
          
          {/* Super Train Body */}
          <div className="relative group">
            <div className={`relative w-32 h-16 rounded-xl shadow-lg border-2 transition-all duration-300 ${
              isHyperloop 
                ? 'bg-gradient-to-r from-blue-100 via-blue-200 to-blue-300 border-blue-400' 
                : 'bg-gradient-to-r from-purple-100 via-purple-200 to-purple-300 border-purple-400'
            }`}>
              
              {/* Futuristic nose cone */}
              <div className={`absolute ${isReversed ? 'right-full' : 'left-full'} top-1/2 transform -translate-y-1/2`}>
                <div className={`w-0 h-0 ${
                  isReversed 
                    ? `border-r-12 ${isHyperloop ? 'border-r-blue-200' : 'border-r-purple-200'} border-t-8 border-b-8 border-t-transparent border-b-transparent`
                    : `border-l-12 ${isHyperloop ? 'border-l-blue-200' : 'border-l-purple-200'} border-t-8 border-b-8 border-t-transparent border-b-transparent`
                }`}></div>
              </div>
              
              {/* Train Label */}
              <div className="absolute inset-0 flex items-center justify-center">
                <span className={`font-bold text-2xl ${
                  isHyperloop ? 'text-blue-800' : 'text-purple-800'
                }`}>
                  {label}
                </span>
              </div>
              
              {/* Futuristic windows */}
              <div className="absolute top-3 left-4 right-4 flex justify-between">
                {[...Array(4)].map((_, i) => (
                  <div key={i} className={`w-4 h-3 rounded-full ${
                    isHyperloop ? 'bg-blue-300' : 'bg-purple-300'
                  }`}></div>
                ))}
              </div>
              
              {/* Jet exhaust when moving */}
              {(speed > 0 || isActive) && (
                <div className={`absolute ${isReversed ? 'right-full mr-2' : 'left-full ml-2'} top-1/2 transform -translate-y-1/2`}>
                  <div className="flex flex-col space-y-1">
                    <div className="h-1 w-12 bg-orange-400 animate-pulse rounded-full"></div>
                    <div className="h-1 w-10 bg-yellow-400 animate-pulse rounded-full"></div>
                    <div className="h-1 w-8 bg-red-400 animate-pulse rounded-full"></div>
                  </div>
                  {/* Jet flame effect */}
                  <div className={`absolute top-1/2 transform -translate-y-1/2 ${isReversed ? 'right-0' : 'left-0'}`}>
                    <div className="text-2xl animate-bounce">🔥</div>
                  </div>
                </div>
              )}
              
              {/* Magnetic levitation indicators */}
              <div className="absolute -bottom-2 left-4 right-4 flex justify-between">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="w-6 h-2 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full animate-pulse"></div>
                ))}
              </div>
              
              {/* Energy field */}
              <div className={`absolute inset-0 rounded-xl opacity-30 ${
                isHyperloop ? 'bg-blue-400' : 'bg-purple-400'
              } animate-pulse`}></div>
            </div>
            
            {/* Scenario label */}
            <div className="text-center mt-3">
              <div className={`font-bold text-lg ${isHyperloop ? 'text-blue-800' : 'text-purple-800'}`}>
                {scenario === 'same-direction' ? '同方向 Same Direction' : '逆方向 Opposite Directions'}
              </div>
              <div className="text-sm text-gray-600">
                {scenario === 'same-direction' ? '→ → (Subtract speeds)' : '→ ← (Add speeds)'}
              </div>
              {scenario === 'opposite-direction' && (
                <div className="mt-2 text-xs text-purple-600 italic">
                  💡 Fun Fact: Moving toward each other = ADD speeds!
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Regular animated train for the track
  const AnimatedTrain = ({ type, direction, speed, distance, label }) => {
    const isHyperloop = type === 'hyperloop';
    const isReversed = direction === 'left';
    
    return (
      <div className={`flex items-center ${isReversed ? 'flex-row-reverse' : ''}`}>
        <div className="relative">
          {/* Train Body */}
          <div className={`relative w-24 h-12 rounded-lg shadow-lg border-2 transition-all duration-300 ${
            isHyperloop 
              ? 'bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600 border-blue-700' 
              : 'bg-gradient-to-r from-purple-400 via-purple-500 to-purple-600 border-purple-700'
          }`}>
            
            {/* Nose cone */}
            <div className={`absolute ${isReversed ? 'right-full' : 'left-full'} top-1/2 transform -translate-y-1/2`}>
              <div className={`w-0 h-0 ${
                isReversed 
                  ? `border-r-8 ${isHyperloop ? 'border-r-blue-500' : 'border-r-purple-500'} border-t-6 border-b-6 border-t-transparent border-b-transparent`
                  : `border-l-8 ${isHyperloop ? 'border-l-blue-500' : 'border-l-purple-500'} border-t-6 border-b-6 border-t-transparent border-b-transparent`
              }`}></div>
            </div>
            
            {/* Label */}
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="font-bold text-lg text-white">{label}</span>
            </div>
            
            {/* Jet exhaust */}
            {speed > 0 && (
              <div className={`absolute ${isReversed ? 'right-full mr-1' : 'left-full ml-1'} top-1/2 transform -translate-y-1/2`}>
                <div className="flex flex-col space-y-0.5">
                  <div className="h-0.5 w-8 bg-orange-400 animate-pulse"></div>
                  <div className="h-0.5 w-6 bg-yellow-400 animate-pulse"></div>
                  <div className="h-0.5 w-4 bg-red-400 animate-pulse"></div>
                </div>
              </div>
            )}
            
            {/* Magnetic levitation */}
            <div className="absolute -bottom-1 left-2 right-2 flex justify-between">
              <div className="w-3 h-1 bg-cyan-400 rounded-full animate-pulse"></div>
              <div className="w-3 h-1 bg-cyan-400 rounded-full animate-pulse"></div>
            </div>
          </div>
          
          {/* Info Panel */}
          <div className={`${isReversed ? 'mr-3' : 'ml-3'} bg-white p-2 rounded-lg shadow-md border`}>
            <div className={`font-bold text-sm ${isHyperloop ? 'text-blue-600' : 'text-purple-600'}`}>
              {isHyperloop ? '🚀 Hyperloop' : '⚡ Maglev'}
            </div>
            <div className="text-xs text-gray-600">{speed} mph</div>
            <div className="text-xs text-gray-500">{distance.toFixed(1)} mi</div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">
            🚀 MathCraft: Jet-Powered Super Train Motion
          </h1>
          <p className="text-xl text-gray-600">Future Transportation Mathematics | ハイパーループ数学</p>
        </div>

        {/* Interactive Train Toggle Buttons */}
        <div className="bg-white rounded-2xl shadow-2xl p-8 mb-8 border border-gray-200">
          <h2 className="text-3xl font-bold mb-8 text-gray-800 text-center">
            🛸 Click the Super Trains to Choose Your Scenario!
          </h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Same Direction - Hyperloop Toggle */}
            <JetSuperTrain
              type="hyperloop"
              direction="right"
              speed={trainBSpeed}
              distance={0}
              label="SAME ↗"
              isActive={scenario === 'same-direction'}
              onClick={() => setScenario('same-direction')}
              scenario="same-direction"
            />

            {/* Opposite Direction - Maglev Toggle */}
            <JetSuperTrain
              type="maglev"
              direction="left"
              speed={trainASpeed}
              distance={0}
              label="OPPOSITE ↔"
              isActive={scenario === 'opposite-direction'}
              onClick={() => setScenario('opposite-direction')}
              scenario="opposite-direction"
            />
          </div>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-xl shadow-xl p-6 mb-6 border border-gray-100">
          <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center gap-2">
            <Zap className="text-yellow-500" />
            🚀 Super Train Parameters
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-3">
              <label className="block text-sm font-bold text-blue-600 mb-2">
                🚀 Hyperloop A Speed: {trainASpeed} mph
                <br />
                <span className="text-xs text-gray-500">磁気浮上式 (Magnetic Levitation)</span>
              </label>
              <input
                type="range"
                min="100"
                max="500"
                value={trainASpeed}
                onChange={(e) => setTrainASpeed(Number(e.target.value))}
                className="w-full h-3 bg-blue-200 rounded-lg appearance-none cursor-pointer"
              />
              <input
                type="number"
                value={trainASpeed}
                onChange={(e) => setTrainASpeed(Number(e.target.value))}
                className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus:border-blue-500 focus:outline-none text-lg"
                min="100"
                max="700"
              />
            </div>
            <div className="space-y-3">
              <label className="block text-sm font-bold text-purple-600 mb-2">
                ⚡ Maglev B Speed: {trainBSpeed} mph
                <br />
                <span className="text-xs text-gray-500">ジェット推進 (Jet Propulsion)</span>
              </label>
              <input
                type="range"
                min="200"
                max="800"
                value={trainBSpeed}
                onChange={(e) => setTrainBSpeed(Number(e.target.value))}
                className="w-full h-3 bg-purple-200 rounded-lg appearance-none cursor-pointer"
              />
              <input
                type="number"
                value={trainBSpeed}
                onChange={(e) => setTrainBSpeed(Number(e.target.value))}
                className="w-full px-4 py-3 border-2 border-purple-300 rounded-lg focus:border-purple-500 focus:outline-none text-lg"
                min="200"
                max="1000"
              />
            </div>
            <div className="space-y-3">
              <label className="block text-sm font-bold text-pink-600 mb-2">
                ⏰ Head Start: {headStart} hours
                <br />
                <span className="text-xs text-gray-500">先発時間 (Launch Delay)</span>
              </label>
              <input
                type="range"
                min="0.5"
                max="5"
                step="0.5"
                value={headStart}
                onChange={(e) => setHeadStart(Number(e.target.value))}
                className="w-full h-3 bg-pink-200 rounded-lg appearance-none cursor-pointer"
              />
              <input
                type="number"
                value={headStart}
                onChange={(e) => setHeadStart(Number(e.target.value))}
                className="w-full px-4 py-3 border-2 border-pink-300 rounded-lg focus:border-pink-500 focus:outline-none text-lg"
                min="0"
                max="10"
                step="0.5"
              />
            </div>
          </div>
        </div>

        {/* Animation */}
        <div className="bg-white rounded-xl shadow-xl p-6 mb-6 border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800">🎬 Live Super Train Animation</h2>
            <div className="flex gap-3">
              <button
                onClick={() => setIsAnimating(!isAnimating)}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-700 text-white rounded-lg hover:from-blue-700 hover:to-purple-800 transition-all shadow-lg text-lg"
              >
                {isAnimating ? <Pause size={24} /> : <Play size={24} />}
                {isAnimating ? '🛑 Stop' : '🚀 Launch'}
              </button>
              <button
                onClick={resetAnimation}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-gray-600 to-gray-700 text-white rounded-lg hover:from-gray-700 hover:to-gray-800 transition-all shadow-lg text-lg"
              >
                <RotateCcw size={24} />
                🔄 Reset
              </button>
            </div>
          </div>

          <div className="relative bg-gradient-to-b from-gray-100 to-gray-200 p-8 rounded-xl border-2 border-gray-300">
            <div className="relative">
              {/* Futuristic Track */}
              <div className="relative w-full h-8 mb-16">
                <div className="w-full h-6 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-lg"></div>
                <div className="absolute top-1 left-0 w-full h-1 bg-cyan-400 rounded-full animate-pulse"></div>
                <div className="absolute bottom-1 left-0 w-full h-1 bg-pink-400 rounded-full animate-pulse"></div>
                {/* Energy nodes */}
                {[...Array(15)].map((_, i) => (
                  <div
                    key={i}
                    className="absolute top-0 w-2 h-6 bg-yellow-400 animate-pulse"
                    style={{ left: `${i * 6.67}%` }}
                  />
                ))}
              </div>

              {/* Distance markers */}
              <div className="flex justify-between text-sm text-gray-700 mb-8 font-mono">
                {[...Array(8)].map((_, i) => (
                  <div key={i} className="text-center">
                    <div className="w-px h-4 bg-gray-400 mx-auto mb-1"></div>
                    <span className="block">{Math.round((i * maxDistance) / 7)} mi</span>
                    <span className="text-xs text-blue-600">
                      {i === 0 ? '🚀 Launch' : i === 7 ? '🏁 Finish' : `Station ${i}`}
                    </span>
                  </div>
                ))}
              </div>

              {/* Animated Super Trains */}
              <div className="relative h-32">
                {/* Train A */}
                <div
                  className="absolute transition-all duration-100 ease-linear"
                  style={{ 
                    left: `${trainAPos}px`,
                    top: '-80px'
                  }}
                >
                  <AnimatedTrain 
                    type="hyperloop" 
                    direction="right" 
                    speed={trainASpeed} 
                    distance={trainADistance} 
                    label="A"
                  />
                </div>

                {/* Train B */}
                <div
                  className="absolute transition-all duration-100 ease-linear"
                  style={{ 
                    left: `${trainBPos}px`,
                    top: '40px'
                  }}
                >
                  <AnimatedTrain 
                    type="maglev" 
                    direction={scenario === 'opposite-direction' ? 'left' : 'right'} 
                    speed={trainBSpeed} 
                    distance={trainBDistance} 
                    label="B"
                  />
                </div>

                {/* Meeting point */}
                {meeting && (
                  <div
                    className="absolute top-0 w-4 h-32 bg-gradient-to-b from-green-400 to-emerald-600 animate-pulse rounded-full"
                    style={{ left: `${(meeting.distance / maxDistance) * 700}px` }}
                  >
                    <div className="absolute -top-12 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg">
                      ⚡ COLLISION POINT
                    </div>
                    <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 text-xs bg-white px-3 py-1 rounded border shadow">
                      {meeting.distance.toFixed(1)} mi
                    </div>
                  </div>
                )}
              </div>

              {/* Enhanced time display */}
              <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
                <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
                  <div className="text-3xl font-bold text-blue-600">{animationTime.toFixed(1)}h</div>
                  <div className="text-sm text-gray-600">⏱️ Elapsed Time</div>
                  <div className="text-xs text-blue-500 mt-1">{(animationTime * 60).toFixed(0)} minutes</div>
                </div>
                {meeting && (
                  <>
                    <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500">
                      <div className="text-3xl font-bold text-green-600">{meeting.time.toFixed(1)}h</div>
                      <div className="text-sm text-gray-600">🎯 Meeting Time</div>
                      <div className="text-xs text-green-500 mt-1">{(meeting.time * 60).toFixed(0)} minutes</div>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-purple-500">
                      <div className="text-3xl font-bold text-purple-600">
                        {scenario === 'same-direction' ? trainBSpeed - trainASpeed : trainASpeed + trainBSpeed}
                      </div>
                      <div className="text-sm text-gray-600">
                        {scenario === 'same-direction' ? '🔄 Relative Speed' : '⚡ Combined Speed'} (mph)
                      </div>
                      <div className="text-xs text-purple-500 mt-1">
                        {scenario === 'same-direction' ? 'Catching Speed' : 'Approach Speed'}
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Calculator */}
        <div className="bg-white rounded-xl shadow-xl p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              <Calculator className="text-indigo-600" />
              🧮 Mathematical Solution
            </h2>
            <button
              onClick={() => setShowCalculations(!showCalculations)}
              className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-700 text-white rounded-lg hover:from-indigo-700 hover:to-purple-800 transition-all shadow-lg text-lg"
            >
              <Calculator size={20} />
              {showCalculations ? '🙈 Hide' : '🤓 Show'} Calculations
            </button>
          </div>

          {showCalculations && meeting && (
            <div className="space-y-6">
              <div className="bg-gradient-to-r from-gray-50 to-gray-100 p-6 rounded-xl border-2 border-gray-200">
                <h3 className="font-bold text-xl mb-4 text-gray-800">📋 Super Train Problem Setup:</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-lg">
                  <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                    <strong>🚀 Hyperloop A:</strong> {trainASpeed} mph, {headStart}-hour head start
                    <br />
                    <span className="text-sm text-gray-600">Magnetic levitation technology</span>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                    <strong>⚡ Maglev B:</strong> {trainBSpeed} mph, {scenario === 'same-direction' ? 'same direction' : 'opposite direction'}
                    <br />
                    <span className="text-sm text-gray-600">Jet propulsion system</span>
                  </div>
                </div>
              </div>

              {scenario === 'same-direction' ? (
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border-2 border-blue-200">
                  <h3 className="font-bold text-xl mb-4 text-blue-800">🎯 Same Direction Solution:</h3>
                  <div className="space-y-4">
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-lg"><strong>Step 1:</strong> Let t = time Maglev B travels</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-lg"><strong>Step 2:</strong> Distance equations:</p>
                      <div className="ml-4 mt-2 font-mono text-blue-700 text-lg">
                        <p>Hyperloop A: {trainASpeed}(t + {headStart}) miles</p>
                        <p>Maglev B: {trainBSpeed}t miles</p>
                      </div>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-lg"><strong>Step 3:</strong> Set distances equal:</p>
                      <div className="ml-4 mt-2 font-mono text-blue-700 text-xl">
                        {trainASpeed}(t + {headStart}) = {trainBSpeed}t
                      </div>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-lg"><strong>Step
