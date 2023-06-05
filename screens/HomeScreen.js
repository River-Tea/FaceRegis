import React, { useEffect, useState } from 'react';
import { View, StyleSheet, Text, TouchableOpacity } from 'react-native';
import { useRoute } from '@react-navigation/native';

const API_BASE_URL = 'http://192.168.1.6:5000';

const HomeScreen = ({ navigation }) => {
    const route = useRoute();
    const { userID } = route.params;
    const [username, setUsername] = useState(userID);

    useEffect(() => {
        getUser();
    }, []);

    const getUser = async () => {
        setUsername(userID);
    };

    const handleLogout = async () => {
        setUsername(null)
        navigation.navigate('Login')
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Welcome, {username}!</Text>
            <TouchableOpacity style={styles.button} onPress={handleLogout}>
                <Text style={styles.buttonText}>Log Out</Text>
            </TouchableOpacity>
        </View>
    );
};

export default HomeScreen

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#fff',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    input: {
        width: '80%',
        height: 40,
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 5,
        padding: 10,
        marginBottom: 10,
    },
    button: {
        width: '80%',
        height: 40,
        backgroundColor: '#007BFF',
        borderRadius: 5,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 10,
    },
    buttonText: {
        color: '#fff',
        fontWeight: 'bold',
    },
});