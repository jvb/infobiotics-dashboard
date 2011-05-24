
package propertybuilder.pattern;

/**
 *
 * @author Ciprian
 */
public enum PatternType {
    UNDEFINED {@Override public String toString() { return "undefined"; } } ,
    PROPERTY {@Override public String toString() { return "property"; } },
    STATE {@Override public String toString() { return "state"; } },
    REWARD {@Override public String toString() { return "reward"; } }
}
