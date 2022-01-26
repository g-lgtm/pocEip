import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from "react-redux";
import { getField } from '../actions/field.actions';
import { isEmpty } from '../Utils';
import FieldCard from './FieldCard';

const Field = () => {
    const [loadField, setLoadField] = useState(true); 
    const dispatch = useDispatch();
    const field = useSelector((state) => state.fieldReducer)
    useEffect(() => {
        if(loadField) {
            dispatch(getField());
            setLoadField(false);
        }
    }, [loadField, dispatch])
    return (
        <div>
        <ul>
            {!isEmpty(field[0]) &&  field.map((field) => {
                return <FieldCard field={field} key={field._id}/>
            })
            }
        </ul>
    </div>
    );
};

export default Field;