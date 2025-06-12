import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Calculator } from 'lucide-react';

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
    const trackWidth = 600;
    const maxDistance = meeting ? Math.max(meeting.distance * 1.3, 300) : 300;

    let trainADistance, trainBDistance;

    if (scenario === 'same-direction') {
      trainADistance = trainASpeed * (animationTime + headStart);
      trainBDistance = animationTime > 0 ? trainBSpeed * animationTime : 0;
    } else {
      trainADistance = trainASpeed * (animationTime + headStart);
      trainBDistance = animationTime > 0 ? trainBSpeed * animationTime : 0;
    }

    const trainAPos = Math.min((trainADistance / maxDistance) * trackWidth, trackWidth - 80);
    let trainBPos;

    if (scenario === 'same-direction') {
      trainBPos = Math.min((trainBDistance / maxDistance) * trackWidth, trackWidth - 80);
    } else {
      trainBPos = Math.max(trackWidth - 80 - (trainBDistance / maxDistance) * trackWidth, 0);
    }

    return { trainAPos, trainBPos, maxDistance, trainADistance, trainBDistance };
  };

  const { trainAPos, trainBPos, maxDistance, trainADistance, trainBDistance } = getTrainPositions();

  return (
    <div className="min-h-screen bg-blue-50 p-4">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-xl shadow-xl mb-8">
        <h2 className="text-3xl font-bold text-blue-700 mb-4">Core Concept: Relative Speed</h2>
        <div className="text-lg text-gray-700 mb-4">
          <p>When two objects (like trains) move on the same path:</p>
          <ul className="list-disc pl-6">
            <li>In the <strong>same direction</strong>: <em>Subtract</em> speeds</li>
            <li>In <strong>opposite directions</strong>: <em>Add</em> speeds</li>
          </ul>
        </div>
        <h3 className="text-2xl font-semibold text-purple-800 mb-2">Same Direction Example</h3>
        <p className="text-gray-700 mb-4">
          Train A leaves a station traveling at 40 mph. Two hours later, Train B leaves the same station traveling at 60 mph. How long will it take Train B to catch up?
        </p>
        <ol className="list-decimal pl-6 text-gray-700 mb-4">
          <li><strong>Define Variables:</strong> Let t = time Train B travels. Train A's time = t + 2</li>
          <li><strong>Equations:</strong> Train A: 40(t + 2), Train B: 60t</li>
          <li><strong>Set equal:</strong> 40(t + 2) = 60t → 40t + 80 = 60t → 80 = 20t → t = 4</li>
          <li><strong>Conclusion:</strong> Train B catches Train A in 4 hours of its own travel time.</li>
        </ol>
        <p className="font-mono text-gray-800 mb-2">
          General Formula: t = (r1 * h) / (r2 - r1)
        </p>
        <h4 className="text-xl font-bold mb-2">Practice Problem</h4>
        <p className="text-gray-700">
          Train A leaves at 50 mph. Train B leaves 3 hours later at 65 mph. <br/>
          t = (50 * 3) / (65 - 50) = 150 / 15 = 10 <br/>
          <strong>Answer:</strong> Train B catches Train A after 10 hours of its own travel, or 13 hours after Train A started.
        </p>

        <h3 className="text-2xl font-semibold text-purple-800 mt-8 mb-2">Opposite Direction Example</h3>
        <p className="text-gray-700 mb-4">
          Train A leaves a station heading east at 40 mph. Train B leaves another station heading west at 60 mph. If the two stations are 300 miles apart, how long will it take for the trains to meet?
        </p>
        <ol className="list-decimal pl-6 text-gray-700 mb-4">
          <li><strong>Define Variables:</strong> Distance = 300 miles, Speeds: 40 mph and 60 mph</li>
          <li><strong>Add speeds:</strong> 40 + 60 = 100 mph</li>
          <li><strong>Solve:</strong> t = 300 / 100 = 3 hours</li>
          <li><strong>Conclusion:</strong> The trains meet after 3 hours.</li>
        </ol>
        <p className="font-mono text-gray-800 mb-2">
          General Formula: t = d / (r1 + r2)
        </p>
      </div>

      {/* The rest of your JSX interface and logic components continue here */}
    </div>
  );
};

export default TrainCalculator;
